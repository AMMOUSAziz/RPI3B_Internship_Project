
# 1 -  connect to MQTT Broker
# > adapt the MQTT_Publisher.py code in order to have a connect function and a disconnect function : in entry an ip
# > ip entered by the user

# Declaration of two needed variables : flame sensor & gas detection ;


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


# Problems : difference in number of iterations in a given period of time needed for button and sending data; 
#  
#
#
#
#
#