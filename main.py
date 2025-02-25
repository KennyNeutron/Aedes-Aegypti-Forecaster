from flask import Flask, jsonify, render_template, send_from_directory
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
from flask import Response

app = Flask(__name__)

# Initialize DS3231
i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)

# Define folders for saving images
IMAGE_FOLDER = "captured_images"
INFERENCE_OUTPUT_FOLDER = "inference_output"
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(INFERENCE_OUTPUT_FOLDER, exist_ok=True)

# Roboflow API settings
API_URL = "https://detect.roboflow.com"
API_KEY = "122aOY67jDoRdfvlcYg6"
MODEL_ID = "mosquito_faa/1"

# Ensure the database path is correct
DATABASE_PATH = 'FAA_DB.db'

# Function to capture an image using Raspberry Pi Camera Module 2
def capture_image():
    now = rtc.datetime  # Get DS3231 RTC time
    date_str = f"{now.tm_year}_{now.tm_mon:02d}_{now.tm_mday:02d}"
    time_period = "AM" if now.tm_hour < 12 else "PM"
    filename = f"{date_str}_{time_period}.jpg"
    image_path = os.path.join(IMAGE_FOLDER, filename)

    try:
        print(f"📸 Capturing image: {image_path}...")
        subprocess.run(["libcamera-still", "-o", image_path, "--width", "1920", "--height", "1080", "--timeout", "1"], check=True)
        print(f"✅ Image saved: {image_path}")
        run_inference_later(image_path, filename)  # Schedule inference in 2 minutes
    except Exception as e:
        print(f"❌ Camera Error: {e}")

# Function to run inference on the captured image
def run_inference(image_path, filename):
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
        if image is None:
            print(f"❌ Error: Unable to read input image {image_path}")
            return

        for pred in predictions:
            x, y, width, height = (
                int(pred["x"]), int(pred["y"]), int(pred["width"]), int(pred["height"])
            )
            confidence = pred["confidence"]
            label = "FAA"
            
            x1, y1, x2, y2 = x - width // 2, y - height // 2, x + width // 2, y + height // 2
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            text = f"{label}: {confidence:.2f}"
            cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        rtc_time = rtc.datetime
        formatted_time = f"{rtc_time.tm_year}-{rtc_time.tm_mon:02d}-{rtc_time.tm_mday:02d} {'AM' if rtc_time.tm_hour < 12 else 'PM'}"
        temperature = rtc.temperature
        info_text = f"{formatted_time} | Temp: {temperature} degC | FAA Count: {faa_count}"
        cv2.putText(image, info_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 255, 0), 2)

        # Save the processed image
        cv2.imwrite(output_path, image)
        print(f"✅ Inference result saved at {output_path}")

        # Log the data to the database
        log_data(formatted_time, faa_count, temperature)

    except Exception as e:
        print(f"❌ Inference Error: {e}")


# Function to delay inference by 2 minutesf
def run_inference_later(image_path, filename):
    print("⏳ Scheduling inference in 2 minutes...")
    threading.Timer(120, run_inference, args=[image_path, filename]).start()

# Function to check time and capture image at exactly 7 AM and 8 PM
def schedule_capture():
    while True:
        now = rtc.datetime  # Get DS3231 RTC time

        if now.tm_hour == 7 and now.tm_min == 0:
            capture_image()
            time.sleep(60)
        elif now.tm_hour == 20 and now.tm_min == 0:
            capture_image()
            time.sleep(60)

        time.sleep(1)

def log_data(datetime_str, faa_count, temperature):
    conn = sqlite3.connect('FAA_DB.db')
    cursor = conn.cursor()
    sql = '''
    INSERT INTO MosquitoData (datetime, faa_count, temperature)
    VALUES (?, ?, ?);
    '''
    cursor.execute(sql, (datetime_str, faa_count, temperature))
    conn.commit()
    conn.close()
    print(f"Data logged for {datetime_str}: FAA Count = {faa_count}, Temp = {temperature}")


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
    """API endpoint to fetch time & temperature from DS3231 RTC."""
    rtc_time = rtc.datetime  # Ensure we fetch DS3231 time directly
    formatted_time = f"{rtc_time.tm_year}-{rtc_time.tm_mon:02d}-{rtc_time.tm_mday:02d} {rtc_time.tm_hour:02d}:{rtc_time.tm_min:02d}:{rtc_time.tm_sec:02d}"
    temperature = rtc.temperature  # Read temperature from DS3231
    
    print(f"📡 DS3231 Time Sent to UI: {formatted_time}")  # Debugging log
    return jsonify({"time": formatted_time, "temperature": temperature})


@app.route('/inference_output')
def inference_output():
    """Serve the inference output page."""
    return render_template("inference_output.html")

@app.route('/inference_images')
def list_inference_images():
    """API endpoint to list inference images."""
    files = [f"/inference_output/{f}" for f in os.listdir(INFERENCE_OUTPUT_FOLDER) if f.endswith(".jpg")]
    return jsonify({"images": files})

@app.route('/inference_output/<filename>')
def get_inference_image(filename):
    """Serve individual inference images."""
    return send_from_directory(INFERENCE_OUTPUT_FOLDER, filename)

@app.route('/data-log')
def data_log():
    """Serve the Data Log page."""
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
    cursor.execute("SELECT datetime, faa_count, temperature FROM MosquitoData ORDER BY datetime DESC")
    data = cursor.fetchall()
    conn.close()

    def generate():
        # Use StringIO to handle CSV data in memory
        import io
        data_stream = io.StringIO()
        csv_writer = csv.writer(data_stream)
        csv_writer.writerow(['Date and Time', 'FAA Count', 'Temperature'])
        for row in data:
            csv_writer.writerow(row)
        data_stream.seek(0)  # Move cursor to the beginning of the stream
        return data_stream.getvalue()

    return Response(
        generate(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=data_log.csv"}
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
