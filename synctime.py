import time
import board
import adafruit_ds3231
import subprocess

def set_system_time_from_rtc(rtc):
    now = rtc.datetime
    # Format the date and time into a string that the date command can understand
    formatted_time = f"{now.tm_year}-{now.tm_mon:02d}-{now.tm_mday:02d} {now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d}"
    # Set the system time using the date command
    subprocess.run(['sudo', 'date', '--set', formatted_time], check=True)
    print(f"System time set from RTC: {formatted_time}")

def set_rtc_time_from_system(rtc):
    # Get the current system time
    now = time.localtime()
    # Set the RTC time to the system time
    rtc.datetime = now
    print(f"RTC time set from system: {time.strftime('%Y-%m-%d %H:%M:%S', now)}")

def main():
    i2c = board.I2C()
    rtc = adafruit_ds3231.DS3231(i2c)

    choice = input("Sync time based on: \n1. Raspberry Pi (System Time) \n2. DS3231 (RTC Time) \nEnter choice (1 or 2): ")
    
    if choice == '1':
        set_rtc_time_from_system(rtc)
    elif choice == '2':
        set_system_time_from_rtc(rtc)
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
