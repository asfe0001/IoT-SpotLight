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
client.connect(address, 1883, 60)
topic_lamp1 = "hska/lamp1/position"
topic_lamp2 = "hska/lamp2/position"



#INIT ultrasonic Sensor
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#INIT LED PWM

LEDPIN = 22
GPIO.setup(LEDPIN, GPIO.OUT) # Set pin 8 to be an output pin and set initial value to low (off)
LED = GPIO.PWM(LEDPIN, 100)

dutyCycleX= 0
LED.start(dutyCycleX)


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
    print(distance)
    return distance


def fadeLED(target, dutyCycleX):
    if target > dutyCycleX:
        for x in range(dutyCycleX, target + 1, 1):
            LED.ChangeDutyCycle(x)
            sleep(0.01)
    else:
        for x in range(dutyCycleX, target - 1, -1):
            LED.ChangeDutyCycle(x)
            sleep(0.01)

    dutyCycleX = target


# variables
pos1 = False
pos2 = False

# subscribe to pos2 here
client.subscribe(topic_lamp2)

#mqtt callback
def on_message_c(client, userdata, message):
    print(message.payload.decode());
    pos2 = message.payload.decode()
client.on_message = on_message_c

# do ForEVER
while True:
    sleep(0.1)
    pos1 = distance() < 200
    if pos1:
       client.publish(topic_lamp1, 1)
       fadeLED(100, dutyCycleX) # LED an
       dutyCycleX = 100
    else:
        client.publish(topic_lamp1, 0)
        if pos2:
            fadeLED(50, dutyCycleX) # LED halb hell
            dutyCycleX = 50
        else:
            fadeLED(0, dutyCycleX) # LED aus
            dutyCycleX = 0
            
    # TO DO: publish pos1
