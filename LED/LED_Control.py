from gpiozero import RGBLED
from time import sleep
from colorzero import Color

# GPIO pin assignments for the RGB LED
red_pin = 19
green_pin =13 
blue_pin = 26

# Initialize the RGB LED with red, green, and blue components connected to their respective GPIO pins
led = RGBLED(red=red_pin, green=green_pin, blue=blue_pin)

# Set the LED to red color (red: 100%, green: 0%, blue: 0%) and wait for 1 second
i=1
while i>0 :
  print(i)
  led.color=(i,i,0.1*i)
  sleep(0.01)
  i=i-0.05
led.off()
