from gpiozero import RGBLED
from time import sleep
from colorzero import Color

# GPIO pin assignments for the RGB LED
red_pin = 5
green_pin = 6
blue_pin = 13

# Initialize the RGB LED with red, green, and blue components connected to their respective GPIO pins
led = RGBLED(red=red_pin, green=green_pin, blue=blue_pin)

# Set the LED to red color (red: 100%, green: 0%, blue: 0%) and wait for 1 second
def setLedColor(r,g,b):
  led.color=(r,g,b)
