import RPi.GPIO as GPIO
import time

BuzzerPin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(BuzzerPin, GPIO.OUT) 
GPIO.setwarnings(False)

global Buzz 
Buzz = GPIO.PWM(BuzzerPin, 440) 
def BuzzStart(): 
  Buzz.start(40) 
def BuzzStop():
  Buzz.stop()



