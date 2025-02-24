from flask import Flask, jsonify, render_template, send_from_directory
import board
import adafruit_ds3231
import time
import os
import threading
import subprocess
import cv2
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Initialize DS3231
i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)

# Define folder for saving images
IMAGE_FOLDER = "captured_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Function to overlay timestamp and temperature on image
def overlay_text(image_path, text):
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Error: Unable to read image {image_path}")
        return
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    position = (50, 50)  # Position of text
    font_scale = 1
    font_color = (0, 0, 255)  # Red color
    thickness = 2
    
    # Put text on the image
    cv2.putText(image, text, position, font, font_scale, font_color, thickness, cv2.LINE_AA)
    cv2.imwrite(image_path, image)

# Function to capture an image using Raspberry Pi Camera Module 2
def capture_image(time_period):
    now = rtc.datetime  # Get time from DS3231
    date_str = f"{now.tm_year}_{now.tm_mon:02d}_{now.tm_mday:02d}"
    filename = f"{date_str}_{time_period}.jpg"
    image_path = os.path.join(IMAGE_FOLDER, filename)
    timestamp = f"{now.tm_year}-{now.tm_mon:02d}-{now.tm_mday:02d} {now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d}"
    temperature = rtc.temperature
    overlay_text_str = f"{timestamp} | Temp: {temperature:.2f}degC"

    # Use libcamera-still to capture an image
    try:
        subprocess.run(["libcamera-still", "-o", image_path, "--width", "1920", "--height", "1080", "--timeout", "1"], check=True)
        overlay_text(image_path, overlay_text_str)
        print(f"✅ Image captured: {image_path}")
    except Exception as e:
        print(f"❌ Camera Error: {e}")

    return image_path

# Function to check time and capture image at exactly 7 AM and 8 PM
def schedule_capture():
    while True:
        now = rtc.datetime  # Get DS3231 RTC time
        if now.tm_hour == 7 and now.tm_min == 0:
            capture_image("AM")
            time.sleep(60)  # Wait 1 minute to prevent multiple captures
        elif now.tm_hour == 20 and now.tm_min == 0:
            capture_image("PM")
            time.sleep(60)  # Wait 1 minute to prevent multiple captures
        time.sleep(1)

# Start the scheduled capture function in a separate thread
threading.Thread(target=schedule_capture, daemon=True).start()

@app.route('/')
def home():
    """Serve the HTML UI."""
    return render_template("index.html")

@app.route('/gallery')
def gallery():
    """Serve the gallery page."""
    return render_template("gallery.html")

@app.route('/captured_images')
def list_captured_images():
    """API endpoint to list captured images."""
    files = [f"/captured_images/{f}" for f in os.listdir(IMAGE_FOLDER) if f.endswith(".jpg")]
    return jsonify({"images": files})

@app.route('/captured_images/<filename>')
def get_captured_image(filename):
    """Serve individual images."""
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/data')
def get_sensor_data():
    """API endpoint to fetch time & temperature from DS3231."""
    rtc_time = rtc.datetime
    formatted_time = f"{rtc_time.tm_year}-{rtc_time.tm_mon:02d}-{rtc_time.tm_mday:02d} {rtc_time.tm_hour:02d}:{rtc_time.tm_min:02d}:{rtc_time.tm_sec:02d}"
    temperature = rtc.temperature
    return jsonify({"time": formatted_time, "temperature": temperature})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
