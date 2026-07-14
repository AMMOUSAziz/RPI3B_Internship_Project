from gpiozero import DigitalInputDevice
import time

# Initialize MQ2 sensor on GPIO17
def getStateOfButton(button = DigitalInputDevice(26)):
   return (button.value == 0) 
