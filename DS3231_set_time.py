import time
import board
import adafruit_ds3231

# Initialize I2C and DS3231
i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)

# Set the current time (Adjust accordingly)
new_time = time.struct_time((2025, 2, 8, 14, 30, 0, 0, -1, -1))
rtc.datetime = new_time

print("DS3231 Time Updated Successfully!")