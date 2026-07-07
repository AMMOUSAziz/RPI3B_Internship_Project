"""
This Raspberry Pi code was developed by newbiely.com
This Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-motion-sensor
"""


import RPi.GPIO as GPIO
import time

# Set the GPIO mode and HC-SR501 PIR motion sensor pin
def getStateOfMotion (PIR_PIN=12):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(PIR_PIN, GPIO.IN)

  try:
	# Read the HC-SR501 PIR motion sensor value
    pir_value = GPIO.input(PIR_PIN)
    # PIR output is high when motion is detected
    GPIO.cleanup()
    return (pir_value==GPIO.HIGH)            

  except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
