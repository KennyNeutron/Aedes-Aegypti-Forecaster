import time
import board
import adafruit_ds3231

# Initialize I2C and DS3231
i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)

# Ask user for new time input
user_input = input("Enter the new time (YYYY-MM-DD HH:MM:SS): ")

try:
    # Convert user input to struct_time
    new_time_struct = time.strptime(user_input, "%Y-%m-%d %H:%M:%S")
    
    # Set the DS3231 time
    rtc.datetime = new_time_struct
    print("✅ DS3231 Time Updated Successfully!")
except ValueError:
    print("❌ Invalid format! Please enter the date and time in YYYY-MM-DD HH:MM:SS format.")
