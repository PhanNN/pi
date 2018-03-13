# Using PWM with RPi.GPIO

import RPi.GPIO as GPIO
import time
import sys
from random import randint
import time
import pysher
import logging

root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)
# from pubnub import Pubnub


pusher = pysher.Pusher('490641')

def  my_func(*args, **kwargs):
    print("processing Args:", args)
    print("processing Kwargs:", kwargs)

def _callback(m, channel):
    print(m)

    dc = m['brightness'] * 10

    if m['item'] == 'light-living':
         living.ChangeDutyCycle(dc)

    elif m['item'] == 'light-porch':
        porch.ChangeDutyCycle(dc)

    elif m['item'] == 'fireplace':
        fire.ChangeDutyCycle(dc)

def _error(m):
    print(m)

def connect_handler(data):
    channel = pusher.subscribe('plan-pi')
    channel.bind('new-data', my_func)

pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

GPIO.setmode(GPIO.BCM)

PIN_LIVING = 23
PIN_PORCH = 17
PIN_FIREPLACE = 27

GPIO.setup(PIN_LIVING,GPIO.OUT)
GPIO.setup(PIN_PORCH,GPIO.OUT)
GPIO.setup(PIN_FIREPLACE,GPIO.OUT)

FREQ = 100 # frequency in Hz
FIRE_FREQ = 30 #  flickering effect

# Duty Cycle (0 <= dc <=100)

living = GPIO.PWM(PIN_LIVING, FREQ)
living.start(0)

porch = GPIO.PWM(PIN_PORCH, FREQ)
porch.start(0)

fire = GPIO.PWM(PIN_FIREPLACE, FIRE_FREQ)
fire.start(0)

# PubNub

# pubnub = Pubnub(publish_key='demo', subscribe_key='demo')

# channel = 'pi-house'

# pubnub.subscribe(channels=channel, callback=_callback, error=_error)

def _offAll():
    living.ChangeDutyCycle(0)
    porch.ChangeDutyCycle(0)
    fire.ChangeDutyCycle(0)

try:
    while 1:
        led = randint(0,2)
#       randDc = randint(30,100)
        _offAll()
        if led == 0:
            living.ChangeDutyCycle(100)
#            print 'green'
        elif led == 1:
            porch.ChangeDutyCycle(100)
#            print 'yellow'
        else:
            fire.ChangeDutyCycle(100)
#            print 'red'
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(1)
