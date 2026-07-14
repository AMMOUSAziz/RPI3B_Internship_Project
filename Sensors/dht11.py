# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time

import adafruit_dht
import board

dht = adafruit_dht.DHT11(board.D17)


    

def getHumidity():
    humidity=dht.humidity
    try:
     while (humidity== None):
         time.sleep(0.2)
         humidity=dht.humidity
     return humidity
    except RuntimeError as e:
        # Reading doesn't always work! Just print error and we'll try again
     print("Reading from DHT failure: ", e.args)

def getTemperature():
    temperature=dht.temperature
    try:
     while (temperature== None):
         time.sleep(0.2)
         temperature=dht.temperature
     return temperature
    except RuntimeError as e:
        # Reading doesn't always work! Just print error and we'll try again
     print("Reading from DHT failure: ", e.args)


        # Print what we got to the REPL
#        toPrint=f"Temp: {temperature} *C \t Humidity: {humidity}%"
#       print(str(toPrint))

        









