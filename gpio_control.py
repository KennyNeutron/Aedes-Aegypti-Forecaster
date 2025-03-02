import RPi.GPIO as GPIO
import time

# Define the GPIO pin number
GPIO_PIN = 23  # Use any available GPIO pin

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering (BCM mode)
GPIO.setup(GPIO_PIN, GPIO.OUT)  # Set GPIO as an output

try:
    while True:
        # Turn ON
        GPIO.output(GPIO_PIN, GPIO.HIGH)
        print("GPIO is ON")
        time.sleep(5)  # Wait for 1 second

        # Turn OFF
        GPIO.output(GPIO_PIN, GPIO.LOW)
        print("GPIO is OFF")
        time.sleep(5)  # Wait for 1 second

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    GPIO.cleanup()  # Reset GPIO settings on exit
