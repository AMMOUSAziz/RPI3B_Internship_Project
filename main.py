import paho.mqtt.client as mqtt
import MQTT_Publisher_sending_messages
import Sensors.motion_sensor as motion_sensor
import Sensors.bh1750 as bh1750
import Sensors.flameSensor as flame_sensor
import Sensors.MQ_2 as MQ_2
import Sensors.dht11 as dht11
import time
#import alert
import threading
import LED.LED_Control as LED
import Buzzer.Buzzer as Buzzer
import Sensors.button as Button
#INITIALIZE THE CLIENT ;
"""

unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish 



"""

unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

mqttc.on_publish = MQTT_Publisher_sending_messages.on_publish

#Connect to MQTT Broker
ip=input("please enter mqtt broker ip :")
mqttc.connect(ip)
mqttc.loop_start()


# 1 -  connect to MQTT Broker
# > ## POSSIBLE IMPROVEMENT : adapt the MQTT_Publisher.py code in order to have a connect function and a disconnect function : in entry an ip

# Declaration of two needed variables : flame sensor & gas detection ;
flame_detected=False 
gas_detected=False 


def bh1750_collect_and_send():
    #print("bh1750 running")
    light=bh1750.main()
    MQTT_Publisher_sending_messages.send_message(mqttc,"light",f'{{"light":{float(light)}}}')
    print("bh1750 collect and send")
    

def dht11_collect_and_send(count=0):
    #print("dht11 temperature collect and send running")
    try: 
     temperature=dht11.getTemperature()
     humidity=dht11.getHumidity()
    except RuntimeError as e: 
     count=count+1
     if count<=3 :
       dht11_temperature_collect_and_send(count)
     return 0
    print("dht11_temperature_collect_and_send")
    
    MQTT_Publisher_sending_messages.send_message(mqttc,"temperature",f'{{"temperature":{float(temperature)}}}')
    MQTT_Publisher_sending_messages.send_message(mqttc,"humidity",f'{{"humidity":{float(humidity)}}}')
"""
def dht11_humidity_collect_and_send(count=0):
    #print("dht 11 humidity collect & send running")
    try: 

    except RuntimeError as e: 
     count=count+1
     if count<=3 : 
       dht11_humidity_collect_and_send(count)
     return 0
    print("dht11_humidity_collect_and_send")
    """
    


def motion_sensor_collect_and_send():
   #print("motion sensor running here")
   motion=motion_sensor.getStateOfMotion()
   MQTT_Publisher_sending_messages.send_message(mqttc,"motion",float(motion))
   print("motion sensor collect and send")



def MQ_2_collect_and_send(anchorTimestamp):
   #print("MQ 2 running ")
   gas=MQ_2.getStateOfGas()
   global gas_detected
   gas_detected=bool(gas)
   if (time.time()-anchorTimestamp)>=2:
     MQTT_Publisher_sending_messages.send_message(mqttc,"gas",f'{{"gas":{float(gas)}}}')
     anchorTimestamp=time.time()
     print("MQ2 collect and send")
   return anchorTimestamp


def flameSensor_collect_and_send(anchorTimestamp):
   #print("flame sensor running")
   flame=flame_sensor.getStateOfFlame()
   global flame_detected
   flame_detected=bool(flame)
   if (time.time()-anchorTimestamp)>=2:
     MQTT_Publisher_sending_messages.send_message(mqttc,"flame",f'{{"flame":{float(flame)}}}')
     anchorTimestamp=time.time()
     print("flame sensor collect and send")
    
   return anchorTimestamp



def alert():
  interrupted=False
  while True : 
   global gas_detected 
   global flame_detected
   print(gas_detected,flame_detected)
   
   if (gas_detected or flame_detected) and (not interrupted) : 
    while not interrupted :
      interrupted=interrupted or Button.getStateOfButton()
      if (not gas_detected) and (not flame_detected) or interrupted:
        break
      
      print("time to panic !")
      LED.setLedColor(1,0,0)
      try :
        Buzzer.BuzzStart()
      
      except TypeError : 
        print("Buzzer didn't Buzz")
      interrupted=interrupted or Button.getStateOfButton()
      time.sleep(1)
  
      LED.setLedColor(0,0,0)
      try :
        Buzzer.BuzzStop()
      except TypeError : 
        print("Buzzer didn't stop")
      time.sleep(0.5)
      if Button.getStateOfButton(): 
          interrupted=True
          print("INTERRUPT ALERT SIGNAL")

   if not gas_detected and not flame_detected:
      interrupted=False
          







def loop_bh1750(): 
  while True: 
    bh1750_collect_and_send()
    time.sleep(2)

def loop_dht11():
  while True:
    dht11_collect_and_send()

    time.sleep(2)

def loop_flameSensor():
  while True :
    anchorTimestamp=time.time()
    anchorTimestamp=flameSensor_collect_and_send(anchorTimestamp)


def loop_MQ_2():
  while True :
    anchorTimestamp=time.time()
    anchorTimestamp=MQ_2_collect_and_send(anchorTimestamp)

def loop_motion_sensor():
  while True :
    motion_sensor_collect_and_send()
    time.sleep(2)

def testingLoop():
  while True : 
    global flame_detected
    global gas_detected
    print(flame_detected,gas_detected)
    time.sleep(1)



#Thread per Sensor sending data & verifying ;
# >  if needed, the task of collecting data could be done or not at the same 
# >  schedule  sending MQTT message (with not doing it when no data is sent) ??
# > to manage collecting data in real time and sending data with an interval, 
#   establish a coundition with the timestamp: establish an anchor timestamp 
#   each time an MQTT message is sent, and put the condition for sending data to if
#   the difference between the actual timestamp and the anchor timestamp is greater than a defined value.
# >  return result that would be available us with concurrent.futures
# >  

#  
# 

# Thread for alert ==> two sensors needed + checks the Button ; 
#  
#
#
#
#
#
try : 

 t_loop_bh1750 = threading.Thread(target=loop_bh1750)
 t_loop_dht11 = threading.Thread(target=loop_dht11)
 t_loop_flameSensor = threading.Thread(target=loop_flameSensor)
 t_loop_MQ_2 = threading.Thread(target=loop_MQ_2)
 t_loop_motion_sensor=threading.Thread(target=loop_motion_sensor)
 t_loop_alert=threading.Thread(target=alert)
 #t_loop_test=threading.Thread(target=testingLoop)

 t_loop_bh1750.start()
 t_loop_dht11.start()
 t_loop_flameSensor.start()
 t_loop_MQ_2.start()
 t_loop_motion_sensor.start()
 t_loop_alert.start()
 #t_loop_test.start()

 t_loop_bh1750.join()
 t_loop_dht11.join()
 t_loop_flameSensor.join()
 t_loop_MQ_2.join()
 t_loop_motion_sensor.join()
 t_loop_alert.join()
 #t_loop_test.join()
except KeyboardInterrupt :
  MQTT_Publisher_sending_messages.disconnect(mqttc)