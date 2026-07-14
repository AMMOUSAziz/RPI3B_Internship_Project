count=0
while true ;do
     if [ $count -lt 2 ];then 
        python3 alert
         else
        python3 MQTT_Publisher.py &
        python3 alert &
     fi
     sleep 0.01
     count=$count+0.01
     done