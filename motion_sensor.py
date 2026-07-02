"""
This Raspberry Pi code was developed by newbiely.com
This Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-motion-sensor
"""


import RPi.GPIO as GPIO
import time

# Set the GPIO mode and HC-SR501 PIR motion sensor pin
GPIO.setmode(GPIO.BCM)
PIR_PIN = 12
GPIO.setup(PIR_PIN, GPIO.IN)

try:
    while True:
        # Read the HC-SR501 PIR motion sensor value
        pir_value = GPIO.input(PIR_PIN)

        # PIR output is high when motion is detected
        if pir_value == GPIO.HIGH:
            print("Motion detected!")
        else:
            print("No motion detected.")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()




