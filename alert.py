import Sensors.flameSensor as flame_sensor
import Sensors.MQ_2 as MQ_2
import LED.LED_Control as LED
import Buzzer.Buzzer as Buzzer
import Sensors.button as Button
import time

while flame_sensor.getStateOfFlame() or MQ_2.getStateOfGas() : 
    LED.setLedColor(1,0,0)
    Buzzer.BuzzStart()

    time.sleep(1)

    LED.setLedColor(0,0,0)
    Buzzer.BuzzStop()
    
    time.sleep(0.5)
    if Button.getStateOfButton: 
        break

