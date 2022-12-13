# system library
import RPi.GPIO as GPIO
import time

# for LED pwm brightness 
from time import sleep # Import the sleep function from the time module

# mqtt library
import paho.mqtt.client as mqtt

# MQTT Daten
username=""
password=""
address="test.mosquitto.org"

# connect
client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(address, 1883, 60)


#INIT ultrasonic Sensor
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

#INIT LED PWM

LEDPIN = 22
GPIO.setup(LEDPIN, GPIO.OUT) # Set pin 8 to be an output pin and set initial value to low (off)
LED = GPIO.PWM(LEDPIN, 100)

dutyCycle = 0
LED.start(dutyCycle)

def fadeLED(int target):
    if target > dutyCycle:
        for x in range(dutyCycle, target + 1, 1):
            LED.ChangeDutyCycle(x)
            sleep(0.01)
    else:
        for x in range(dutyCycle, target - 1, -1):
            LED.ChangeDutyCycle(x)
            sleep(0.01)

    dutyCycle = target


#variables
pos1 = False
pos2 = False

# TO DO: subscribe to pos2 here

#do ForEVER
while True:
    pos1 = distance() < 200
    if pos1:
       fadeLED(100) # LED an
    else:
        if pos2:
            fadeLED(50) # LED halb hell
        else:
            fadeLED(0) # LED aus

    # TO DO: publish pos1
