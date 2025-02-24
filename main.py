from flask import Flask, jsonify
import board
import adafruit_ds3231
import time

app = Flask(__name__)

# Initialize DS3231
i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)


@app.route("/data")
def get_sensor_data():
    """API endpoint to fetch time & temperature from DS3231"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    temperature = rtc.temperature
    return jsonify({"time": current_time, "temperature": temperature})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
