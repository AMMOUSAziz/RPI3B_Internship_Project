
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


"""
import RPi.GPIO as GPIO
import threading

_lock = threading.Lock()

BUZZER_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

_buzz_pwm = GPIO.PWM(BUZZER_PIN, 440)  # frequency only
_started = False

def BuzzStart(duty=50):
    global _started
    with _lock:
        if not _started:
            _buzz_pwm.start(duty)   # start ONCE
            _started = True
        else:
            _buzz_pwm.ChangeDutyCycle(duty)  # just update duty

def BuzzStop():
    with _lock:
        # safer than stop() in tight loops/threads:
        # turning duty to 0 silences the buzzer without killing the PWM backend
        _buzz_pwm.ChangeDutyCycle(0)"""