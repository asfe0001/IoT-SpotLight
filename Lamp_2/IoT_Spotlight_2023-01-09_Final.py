#Code for "IoT Spotlight" by Gruppe 2

from paho.mqtt import client as mqtt
import json #import json library
import time
import threading
import logging
import os
import datetime #import datetime library
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# -----------------------

TRIGGER_PIN = 23
LED_PIN = 24
Lamp_ontime = 5
delayTime = 5

TOPIC_SELF = 'lamp2'
PWM_FREQ = 1000
PWM_OFF = 0
PWM_OTHER = 20
PWM_SELF = 100

cloud_state = 0
local_state = 0
topic_lamp1 = "hska/lamp1/position"
topic_lamp3 = "hska/lamp3/position"
state_lamp1 = 0
state_lamp3 = 0

#-------------------------
print("--- Script startet ---")

GPIO.setup(TRIGGER_PIN, GPIO.IN, pull_up_down = GPIO.PUD_OFF)
GPIO.setup(LED_PIN, GPIO.OUT, pull_up_down = GPIO.PUD_OFF)
led_pwm = GPIO.PWM(LED_PIN, PWM_FREQ)
led_pwm.start(0)
GPIO.output(LED_PIN, GPIO.HIGH)

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("hska/lamp1/position") #subscribe to topic
    #client.subscribe("hska/lamp2/position") #subscribe to topic
    client.subscribe("hska/lamp3/position") #subscribe to topic
    
def on_message(client, userdata, msg):
        print(f"Received {msg.payload.decode()} from {msg.topic} topic")
#         if (msg.topic == topic_lamp1):
#             state_lamp1 = msg.payload.decode()
#             
#         if (msg.topic == topic_lamp3):
#             state_lamp3 = msg.payload.decode()    
#         
#         if ((state_lamp1 == 0) and (state_lamp3 == 0)):
#             led_pwm.ChangeDutyCycle(PWM_OFF)
        
        if (msg.topic == topic_lamp3):
            if(msg.payload.decode() == "0"):
                led_pwm.ChangeDutyCycle(PWM_OFF)
        
        error = 0
        temp = -1
        try:
            temp = int(msg.payload.decode())
        except ValueError:
            print("Someone tried to f*ck up the thread")
            error = 1
        if (error != 1):
            cloud_state = temp
        else:
            cloud_state = -1
        print(cloud_state)
        if (cloud_state == 1):
            led_pwm.ChangeDutyCycle(PWM_OTHER)
            #time.sleep(Lamp_ontime)
        

def thread_function(name):
    logging.info("Thread %s: starting", name)
    client.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)
    logging.info("Thread %s: finishing", name)

broker_address="test.mosquitto.org" #broker adress
client = mqtt.Client(TOPIC_SELF) #create new instance
client.on_connect = on_connect  # Define callback function for successful connection
client.connect(broker_address) #connect to broker

timestamp = str(datetime.datetime.now()) #define timestamp in string format

client.on_message=on_message  #attach on_message function to a callback function

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    logging.info("Main    : all done")

#GPIO.output(LED_PIN, GPIO.HIGH)

while 1:
    
    #print ("local_State:", local_state)
    # Ausgabe auf die Konsole
    if GPIO.input(TRIGGER_PIN) == False:
        if local_state == 1:
            print ("Reset!")
            client.publish("hska/" + TOPIC_SELF + "/position", 0)
            #GPIO.output(LED_PIN, GPIO.LOW)
            local_state = 0
    else:
        print ("Triggered!")
        client.publish("hska/" + TOPIC_SELF + "/position", 1)
        #GPIO.output(LED_PIN, GPIO.HIGH)
        local_state = 1
        led_pwm.ChangeDutyCycle(PWM_SELF)
        #time.sleep(Lamp_ontime)
        #client.publish("hska/" + "lamp3" + "/position", 1)
        print ("-------------------")
 
        # Reset + Delay
        #button_pressed = False
        #time.sleep(0.001)
        
print("--- Script ended ---")

#Multithreading code inspired by https://realpython.com/intro-to-python-threading/