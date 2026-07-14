count=0
while true ;do
     if [ $count -ls 2 ];then 
        python3 alert
     fi
     else
        python3 MQTT_Publisher.py &
        python3 alert &
     fi
     sleep 0.01
     count=$count+0.01