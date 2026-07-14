import paho.mqtt.client as mqtt
import MQTT_Publisher_sending_messages
import Sensors.motion_sensor as motion_sensor
import Sensors.bh1750 as bh1750
import Sensors.flameSensor as flame_sensor
import Sensors.MQ_2 as MQ_2
import Sensors.dht11 as dht11
import time
import alert
import threading

#INITIALIZE THE CLIENT ;
unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish 

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
    light=bh1750.main()
    MQTT_Publisher_sending_messages.send_message(mqttc,"light",f'{{"light":{float(light)}}}')
    time.sleep(2)

def dht11_temperature_collect_and_send(count=0):
    try: 
     temperature=dht11.getTemperature()
    except RuntimeError as e: 
     count=count+1
     if count<=3 :
       dht11_temperature_collect_and_send(count)
     return 0
    
    MQTT_Publisher_sending_messages.send_message(mqttc,"temperature",f'{{"temperature":{float(temperature)}}}')
    time.sleep(2)

def dht11_humidity_collect_and_send(count=0):
    try: 
     humidity=dht11.getHumidity()
    except RuntimeError as e: 
     count=count+1
     if count<=3 : 
       dht11_humidity_collect_and_send(count)
     return 0
    
    MQTT_Publisher_sending_messages.send_message(mqttc,"humidity",f'{{"humidity":{float(humidity)}}}')
    time.sleep(2)

def motion_sensor_collect_and_send():
   motion=motion_sensor.getStateOfMotion
   MQTT_Publisher_sending_messages.send_message(mqttc,"motion",float(motion))
   time.sleep(2)

def MQ_2_collect_and_send(anchorTimestamp):
   gas=MQ_2.getStateOfGas()
   if (time.time()-anchorTimestamp)>=2:
     MQTT_Publisher_sending_messages.send_message(mqttc,"gas",f'{{"gas":{float(gas)}}}')
     anchorTimestamp=time.time()
    
   return [bool(gas),anchorTimestamp]


def flameSensor_collect_and_send(anchorTimestamp):
   flame=flame_sensor.getStateOfFlame()
   if (time.time()-anchorTimestamp)>=2:
     MQTT_Publisher_sending_messages.send_message(mqttc,"flame",f'{{"flame":{float(flame)}}}')
     anchorTimestamp=time.time()
    
   return [bool(flame),anchorTimestamp]





def loop_bh1750(): 
  while True: 
    bh1750_collect_and_send()

def loop_dht11():
  while True:
    dht11_humidity_collect_and_send()
    dht11_temperature_collect_and_send()

def loop_flameSensor():
  while True :
    anchorTimestamp=time.time()
    [a,b]=flameSensor_collect_and_send(anchorTimestamp)
    global flame_detected 
    flame_detected=a
    anchorTimestamp=b 

def loop_MQ_2():
  while True :
    anchorTimestamp=time.time()
    [a,b]=MQ_2_collect_and_send(anchorTimestamp)
    global gas_detected 
    gas_detected=a
    anchorTimestamp=b 

def loop_motion_sensor():
  while True :
    motion_sensor_collect_and_send()




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


 t_loop_bh1750.start()
 t_loop_dht11.start()
 t_loop_flameSensor.start()
 t_loop_MQ_2.start()
 t_loop_motion_sensor.start()
 t_loop_alert.start()

 t_loop_bh1750.join()
 t_loop_dht11.join()
 t_loop_flameSensor.join()
 t_loop_MQ_2.join()
 t_loop_motion_sensor.join()
 t_loop_alert.join()

except KeyboardInterrupt :
  MQTT_Publisher_sending_messages.disconnect(mqttc)