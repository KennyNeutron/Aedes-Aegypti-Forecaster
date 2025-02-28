from flask import Flask, jsonify, render_template, send_from_directory, Response, request
import board
import adafruit_ds3231
import time
import os
import threading
import requests
import cv2
import numpy as np
from datetime import datetime
import subprocess
import sqlite3
import csv

app = Flask(__name__)

# Initialize the DS3231 real-time clock
i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)

# Directories for storing images
IMAGE_FOLDER = "captured_images"
INFERENCE_OUTPUT_FOLDER = "inference_output"
TEST_INFERENCE_FOLDER = "system_test"
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(INFERENCE_OUTPUT_FOLDER, exist_ok=True)

# Configuration for Roboflow API
API_URL = "https://detect.roboflow.com"
API_KEY = "122aOY67jDoRdfvlcYg6"
MODEL_ID = "mosquito_faa/1"

# Database file path
DATABASE_PATH = 'FAA_DB.db'

# Set a password for clearing the database (Change this in the environment settings)
CLEAR_DB_PASSWORD = os.getenv('CLEAR_DB_PASSWORD', 'FAA_Forecaster2025')

disable_schedule = False  # Flag to enable/disable scheduled capture

def capture_image():
    """Captures an image using the Raspberry Pi Camera Module 2 at scheduled times."""
    now = rtc.datetime
    date_str = f"{now.tm_year}_{now.tm_mon:02d}_{now.tm_mday:02d}"
    time_period = "AM" if now.tm_hour < 12 else "PM"
    filename = f"{date_str}_{time_period}.jpg"
    image_path = os.path.join(IMAGE_FOLDER, filename)

    try:
        print(f"📸 Capturing image: {image_path}...")
        subprocess.run(["libcamera-still", "-o", image_path, "--width", "1920", "--height", "1080", "--timeout", "1"], check=True)
        print(f"✅ Image saved: {image_path}")
        run_inference_later(image_path, filename)
    except Exception as e:
        print(f"❌ Camera Error: {e}")

def run_inference(image_path, filename):
    """Processes images to detect and count mosquito presence."""
    output_filename = f"output_{filename}"
    output_path = os.path.join(INFERENCE_OUTPUT_FOLDER, output_filename)

    try:
        print(f"🚀 Running inference on {image_path}...")
        response = requests.post(
            f"{API_URL}/{MODEL_ID}?api_key={API_KEY}",
            files={"file": open(image_path, "rb")}
        )
        if response.status_code != 200:
            print(f"❌ Error: Failed to process image - {response.text}")
            return

        result = response.json()
        predictions = result.get("predictions", [])
        faa_count = len(predictions)
        print(f"✅ Total FAA detected: {faa_count}")

        image = cv2.imread(image_path)
        for pred in predictions:
            x, y, width, height = (
                int(pred["x"]), int(pred["y"]), int(pred["width"]), int(pred["height"])
            )
            cv2.rectangle(image, (x - width // 2, y - height // 2), (x + width // 2, y + height // 2), (255, 0, 0), 2)
            cv2.putText(image, f"FAA: {pred['confidence']:.2f}", (x - width // 2, y - height // 2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        timestamp = f"{rtc.datetime.tm_year}-{rtc.datetime.tm_mon:02d}-{rtc.datetime.tm_mday:02d} {'AM' if rtc.datetime.tm_hour < 12 else 'PM'}"
        info_text = f"{timestamp} | FAA Count: {faa_count} | Temp: {rtc.temperature:.1f} degC"
        cv2.putText(image, info_text, (10, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imwrite(output_path, image)
        print(f"✅ Inference result saved at {output_path}")
        log_data(f"{rtc.datetime.tm_year}-{rtc.datetime.tm_mon:02d}-{rtc.datetime.tm_mday:02d} {'AM' if rtc.datetime.tm_hour < 12 else 'PM'}", faa_count, rtc.temperature)

    except Exception as e:
        print(f"❌ Inference Error: {e}")

def run_inference_later(image_path, filename):
    """Delays the inference process to allow for any post-capture processing."""
    threading.Timer(30, run_inference, args=[image_path, filename]).start()
    print("⏳ Scheduling inference in 30 seconds...")

def schedule_capture():
    """Schedules image capture at 7 AM and 8 PM daily, but can be disabled."""
    global disable_schedule
    while True:
        print(f"⏰ Current Time: {rtc.datetime.tm_hour}:{rtc.datetime.tm_min}, Schedule Disabled: {disable_schedule}")  # Debugging
        if not disable_schedule:  # Only run if NOT disabled
            #print("schedule_capture is running...")  # Debugging
            now = rtc.datetime
            if now.tm_hour == 7 and now.tm_min == 0 or now.tm_hour == 20 and now.tm_min == 0:
                print("📸 Triggering scheduled capture...")
                capture_image()
                funct_disable_scheduled_capture()
                time.sleep(60)  # Prevents repeated captures
            else:
                funct_enable_schedule_capture()
        time.sleep(6)

def funct_disable_scheduled_capture():
    global disable_schedule
    disable_schedule = True

def funct_enable_schedule_capture():
    global disable_schedule
    disable_schedule = False

@app.route('/disable_schedule', methods=['POST'])
def disable_schedule_capture():
    """Disables the scheduled capture temporarily."""
    global disable_schedule
    disable_schedule = True
    print("🚫 Scheduled capture DISABLED!")
    return jsonify({"status": "Disabled"})

@app.route('/enable_schedule', methods=['POST'])
def enable_schedule_capture():
    """Re-enables the scheduled capture."""
    global disable_schedule
    disable_schedule = False
    print("✅ Scheduled capture ENABLED!")
    return jsonify({"status": "Enabled"})

def log_data(datetime_str, faa_count, temperature):
    """Logs mosquito data into the database."""
    conn = sqlite3.connect('FAA_DB.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO MosquitoData (datetime, faa_count, temperature) VALUES (?, ?, ?);", (datetime_str, faa_count, temperature))
    conn.commit()
    conn.close()
    print(f"Data logged for {datetime_str}: FAA Count = {faa_count}, Temp = {temperature}")

# Application routes
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

@app.route('/captured_images')
def list_captured_images():
    files = [f"/captured_images/{f}" for f in os.listdir(IMAGE_FOLDER) if f.endswith(".jpg")]
    return jsonify({"images": files})

@app.route('/captured_images/<filename>')
def get_captured_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/data')
def get_sensor_data():
    return jsonify({"time": f"{rtc.datetime.tm_year}-{rtc.datetime.tm_mon:02d}-{rtc.datetime.tm_mday:02d} {rtc.datetime.tm_hour:02d}:{rtc.datetime.tm_min:02d}:{rtc.datetime.tm_sec:02d}", "temperature": rtc.temperature})

@app.route('/inference')
def inference_output():
    return render_template("inference.html")

@app.route('/inference_images')
def list_inference_images():
    files = [f"/inference_output/{f}" for f in os.listdir(INFERENCE_OUTPUT_FOLDER) if f.endswith(".jpg")]
    return jsonify({"images": files})

@app.route('/inference_output/<filename>')
def get_inference_image(filename):
    return send_from_directory(INFERENCE_OUTPUT_FOLDER, filename)

@app.route('/data-log')
def data_log():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT datetime, faa_count, temperature FROM MosquitoData ORDER BY datetime DESC")
    data = cursor.fetchall()
    conn.close()
    return render_template('data_log.html', data=data)

@app.route('/download-data')
def download_data():
    conn = sqlite3.connect('FAA_DB.db')
    cursor = conn.cursor()
    cursor.execute("SELECT datetime, temperature, faa_count FROM MosquitoData ORDER BY datetime DESC")
    data = cursor.fetchall()
    conn.close()

    def generate():
        import io
        data_stream = io.StringIO()
        csv_writer = csv.writer(data_stream)
        csv_writer.writerow(['Date and Time', 'Temperature', 'FAA Count'])
        for row in data:
            csv_writer.writerow(row)
        data_stream.seek(0)
        return data_stream.getvalue()

    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=FAA_DataLog.csv"})

@app.route('/clear-data', methods=['POST'])
def clear_data():
    data = request.json
    password = data.get('password', '')

    if password != CLEAR_DB_PASSWORD:
        return jsonify({'status': 'Incorrect password'}), 403

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM MosquitoData")
    conn.commit()
    conn.close()

    return jsonify({'status': 'Database cleared'})


@app.route('/RunTest')
def RunTest():
    return render_template("RunTest.html")

@app.route('/RunTest_Images')
def list_RunTest_Images():
    """Lists the latest image from the system_test folder"""
    try:
        files = [f for f in os.listdir(TEST_INFERENCE_FOLDER) if f.endswith(".jpg")]
        print("Files in system_test:", files)  # Debugging print

        if not files:
            return jsonify({"images": []})  # Return empty if no images exist

        latest_image = sorted(files, reverse=True)[0]  # Get the latest image
        image_url = f"/system_test/{latest_image}"  # Adjusted URL format
        print("Serving image:", image_url)  # Debugging print
        return jsonify({"images": [image_url]})
    except Exception as e:
        print("Error accessing system_test folder:", str(e))  # Debugging print
        return jsonify({"error": str(e)})

@app.route('/system_test/<filename>')
def get_RunTest_Images(filename):
    """Serves images from the system_test folder"""
    return send_from_directory(TEST_INFERENCE_FOLDER, filename)

@app.route('/RunTest_Capture', methods=['POST'])
def RunTest_Capture():
    """Deletes old images, captures a new one, and saves it to system_test/"""
    try:
        # Step 1: Delete the old image
        files = [f for f in os.listdir(TEST_INFERENCE_FOLDER) if f.endswith(".jpg")]
        for file in files:
            os.remove(os.path.join(TEST_INFERENCE_FOLDER, file))
        print("🗑️ Deleted old image(s) in system_test.")

        # Step 2: Capture a new image
        now = rtc.datetime
        filename = f"RunTest_{now.tm_year}_{now.tm_mon:02d}_{now.tm_mday:02d}_{now.tm_hour:02d}_{now.tm_min:02d}.jpg"
        image_path = os.path.join(TEST_INFERENCE_FOLDER, filename)

        print(f"📸 Capturing new image: {image_path}...")
        subprocess.run(["libcamera-still", "-o", image_path, "--width", "1920", "--height", "1080", "--timeout", "1"], check=True)
        print("✅ Image captured and saved.")

        return jsonify({"status": "Captured", "image": f"/system_test/{filename}"})

    except Exception as e:
        print(f"❌ Capture Error: {e}")
        return jsonify({"status": "Error", "error": str(e)})

if __name__ == '__main__':
    threading.Thread(target=schedule_capture, daemon=True).start()
    print("🚀 Starting Flask server...")
    print(f"schedule_capture status: {disable_schedule}")
    app.run(host='0.0.0.0', port=5000, debug=True)