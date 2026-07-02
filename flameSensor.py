from gpiozero import DigitalInputDevice
import time

#Flame_Sensor on GPIO17
flameSensor = DigitalInputDevice(17)

while True:
   # Detect gas presence (LOW signal indicates flame)
   if flameSensor.value == 0:
      print("Flame detected!")
   else:
      print("No flame detected.")

   # Delay between readings
   time.sleep(1)
