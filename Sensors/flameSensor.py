from gpiozero import DigitalInputDevice
import time

#Flame_Sensor on GPIO17

def getStateOfFlame (flameSensor = DigitalInputDevice(22)):
   # Detect gas presence (LOW signal indicates flame)
   return(flameSensor.value == 0) #True means that flame is detected ; False means flame is not detected

