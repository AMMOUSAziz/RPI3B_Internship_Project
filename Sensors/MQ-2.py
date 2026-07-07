from gpiozero import DigitalInputDevice
import time

# Initialize MQ2 sensor on GPIO17
def getStateOfGas(mq2 = DigitalInputDevice(27)):
   return (mq2.value == 0) #True means that gas is detected ; False means gas is not detected

