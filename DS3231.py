# this is a code from Rasberry Pi 4
import time
import board
import adafruit_ds3231

# Initialize I2C and DS3231
i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)

# Read time from DS3231
t = rtc.datetime
print(
    f"Current DS3231 Time: {t.tm_year}-{t.tm_mon:02d}-{t.tm_mday:02d} {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}"
)
