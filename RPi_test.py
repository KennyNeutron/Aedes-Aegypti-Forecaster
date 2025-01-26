import os
import time
import RPi.GPIO as GPIO
from datetime import datetime

# GPIO Setup
LED_PIN = 17  # Replace with the GPIO pin number where your LED is connected
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)


def blink_led():
    print("Blinking LED...")
    for i in range(10):  # Blink 10 times
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)


def get_cpu_temperature():
    try:
        # Read the CPU temperature from the system
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000.0  # Temperature is given in millidegree Celsius
        return temp
    except FileNotFoundError:
        return "Unable to read CPU temperature"


def get_system_info():
    print("Gathering system information...")
    system_info = {
        "Hostname": os.uname().nodename,
        "OS": os.uname().sysname,
        "Release": os.uname().release,
        "Version": os.uname().version,
        "Architecture": os.uname().machine,
    }
    return system_info


def test_gpio_input():
    print("Testing GPIO input...")
    GPIO.setup(LED_PIN, GPIO.IN)
    state = GPIO.input(LED_PIN)
    GPIO.setup(LED_PIN, GPIO.OUT)  # Reset the pin back to output
    return "HIGH" if state else "LOW"


def main():
    print("Starting Raspberry Pi Test Script...")
    try:
        # Blink LED
        blink_led()

        # Get CPU temperature
        cpu_temp = get_cpu_temperature()
        print(f"CPU Temperature: {cpu_temp}°C")

        # Get system information
        system_info = get_system_info()
        print("\nSystem Information:")
        for key, value in system_info.items():
            print(f"{key}: {value}")

        # Test GPIO input state
        gpio_state = test_gpio_input()
        print(f"GPIO Pin {LED_PIN} is currently: {gpio_state}")

        print("\nTest Completed!")
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    finally:
        GPIO.cleanup()
        print("GPIO cleanup done. Exiting.")


if __name__ == "__main__":
    main()
