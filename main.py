from flask import Flask, jsonify, render_template, send_from_directory
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

# Define folders for saving images
IMAGE_FOLDER = "captured_images"
INFERENCE_OUTPUT_FOLDER = "inference_output"
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(INFERENCE_OUTPUT_FOLDER, exist_ok=True)

# Function to find the latest captured image
def get_latest_image():
    images = sorted(
        [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(".jpg")],
        key=lambda x: os.path.getmtime(os.path.join(IMAGE_FOLDER, x)),
        reverse=True,
    )
    return images[0] if images else None

# Function to run inference on the latest image
def run_inference():
    latest_image = get_latest_image()
    if not latest_image:
        print("❌ No captured images found for inference.")
        return

    input_path = os.path.join(IMAGE_FOLDER, latest_image)
    output_filename = f"output_{latest_image}"
    output_path = os.path.join(INFERENCE_OUTPUT_FOLDER, output_filename)

    try:
        print(f"🚀 Running inference on {input_path}...")
        result = subprocess.run(
            ["python3", "inference_hosted_api.py", input_path, output_path],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ Inference completed. Output saved at {output_path}")
        print(f"🔍 Inference Log:\n{result.stdout}")
        if result.stderr:
            print(f"⚠️ Inference Error Log:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Inference Error: {e}")
        print(f"⚠️ Error Output:\n{e.stderr}")

# Function to check time and capture image at exactly 7 AM and 8 PM
def schedule_capture():
    while True:
        now = rtc.datetime  # Get DS3231 RTC time

        if now.tm_hour == 7 and now.tm_min == 0:
            print("📸 Capturing image at 7:00 AM...")
            run_inference_later()  # Schedule inference at 7:02 AM
            time.sleep(60)
        elif now.tm_hour == 20 and now.tm_min == 0:
            print("📸 Capturing image at 8:00 PM...")
            run_inference_later()  # Schedule inference at 8:02 PM
            time.sleep(60)

        time.sleep(1)

# Function to delay inference by 2 minutes
def run_inference_later():
    print("⏳ Scheduling inference in 2 minutes...")
    threading.Timer(120, run_inference).start()

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
