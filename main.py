from flask import Flask, jsonify, render_template
import board
import adafruit_ds3231
import time
import os
import threading
import subprocess
from datetime import datetime

app = Flask(__name__)

# Initialize DS3231
i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)

# Define folder for saving images
IMAGE_FOLDER = "captured_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Function to capture an image using Raspberry Pi Camera Module 2
def capture_image():
    now = rtc.datetime  # Get time from DS3231
    filename = f"{now.tm_year}-{now.tm_mon:02d}-{now.tm_mday:02d}_{now.tm_hour:02d}-{now.tm_min:02d}-{now.tm_sec:02d}.jpg"
    image_path = os.path.join(IMAGE_FOLDER, filename)

    # Use libcamera-still to capture an image
    try:
        subprocess.run(["libcamera-still", "-o", image_path, "--width", "1920", "--height", "1080", "--timeout", "1"], check=True)
        print(f"✅ Image captured: {image_path}")
    except Exception as e:
        print(f"❌ Camera Error: {e}")

    return image_path

# Function to check time and capture image at exactly 7 AM
def schedule_capture():
    while True:
        now = rtc.datetime  # Get DS3231 RTC time
        if now.tm_hour == 7 and now.tm_min == 0:  # Check if it's 7:00 AM
            capture_image()
            time.sleep(60)  # Wait 1 minute to prevent multiple captures
        time.sleep(1)

# Start the scheduled capture function in a separate thread
threading.Thread(target=schedule_capture, daemon=True).start()

@app.route('/')
def home():
    """Serve the HTML UI."""
    return render_template("index.html")

@app.route('/data')
def get_sensor_data():
    """API endpoint to fetch time & temperature from DS3231."""
    rtc_time = rtc.datetime
    formatted_time = f"{rtc_time.tm_year}-{rtc_time.tm_mon:02d}-{rtc_time.tm_mday:02d} {rtc_time.tm_hour:02d}:{rtc_time.tm_min:02d}:{rtc_time.tm_sec:02d}"
    temperature = rtc.temperature
    return jsonify({"time": formatted_time, "temperature": temperature})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
