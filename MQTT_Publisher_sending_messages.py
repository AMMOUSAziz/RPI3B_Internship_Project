import time
import paho.mqtt.client as mqtt
def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        if userdata is not None : 
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

def send_message(mqttc,topic,messageContent,unacked_publish=set()): 
      message = mqttc.publish(topic, messageContent, qos=1)
      unacked_publish.add(message.mid)
      while len(unacked_publish):
         time.sleep(0.1)
      message.wait_for_publish()

def disconnect(mqttc):
  mqttc.disconnect()
  mqttc.loop_stop()
