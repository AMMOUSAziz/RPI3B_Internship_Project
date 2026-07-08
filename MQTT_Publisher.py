import time
import paho.mqtt.client as mqtt
import Sensors.motion_sensor as motion_sensor
import Sensors.bh1750 as bh1750
import Sensors.flameSensor as flame_sensor
import Sensors.MQ_2 as MQ_2
def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")

unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish 

mqttc.user_data_set(unacked_publish)
mqttc.connect("192.168.1.175")
mqttc.loop_start()
try :
 while True : 
# Our application produce some messages
  motion=motion_sensor.getStateOfMotion()
  flame=flame_sensor.getStateOfFlame()
  gas=MQ_2.getStateOfGas()
  light=bh1750.main()
  looping_list=[]

  msg_motion_info = mqttc.publish("motion", str(motion), qos=1)
  unacked_publish.add(msg_motion_info.mid)
  looping_list.append(msg_motion_info)

  msg_flame_info = mqttc.publish("flame", str(flame), qos=1)
  unacked_publish.add(msg_flame_info.mid)
  looping_list.append(msg_flame_info)

  msg_gas_info = mqttc.publish("gas", str(gas),qos=1)
  unacked_publish.add(msg_gas_info)
  looping_list.append(msg_gas_info)

  msg_light_info=mqttc.publish("light",str(light),gos=1)
  unacked_publish.add(msg_light_info)
  looping_list.append(msg_light_info)



# Wait for all message to be published
  while len(unacked_publish):
     time.sleep(3)

# Due to race-condition described above, the following way to wait for all publish is safer
  for message in looping_list :
     message.wait_for_publish()
except KeyboardInterrupt : 
 mqttc.disconnect()
 mqttc.loop_stop()


