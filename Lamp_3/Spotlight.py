#cph.ka-wlan.de/login

import RPi.GPIO as gpio
import paho.mqtt.client as mqtt
import time

#pinbelegug
sensor = 26;
led = 17;




#mqtt
user = "";
password = "";
address = "test.mosquitto.org";
topic_l3 = "hska/lamp3/position";
topic_l2 ="hska/lamp2/position";
positive = "1";
negative = "0";

l2_value = "";

#mqtt callback
def on_connect_c(client, userdata, flags, rc):
    print("Connected");

    
def on_message_c(client, userdata, message):
    
    if (message.topic == topic_l2):
        global l2_value
        l2_value = message.payload.decode("utf-8");
    

#pin setup

gpio.setmode(gpio.BCM);
gpio.setup(sensor, gpio.IN);
gpio.setup(led, gpio.OUT);

#pwm init
D2A = gpio.PWM(led, 60);
D2A.start(0);

#mqtt setup
client = mqtt.Client("HKA_Lamp3");
client.on_connect = on_connect_c;
client.on_message = on_message_c;
client.connect(address);

client.subscribe(topic_l2);
client.subscribe(topic_l3);

value = 0;
lastVal = value;
lastL2value = negative;
 
 
#int sensor
value = gpio.input(sensor);
client.publish(topic_l3, not value);

client.loop_start();


while(1):
    value = not (gpio.input(sensor));
     
    
    #publish and led update
    if (lastVal != value):
        if (value):
            D2A.ChangeDutyCycle(100);
            client.publish(topic_l3, positive);
        else:
            D2A.ChangeDutyCycle(0);
            client.publish(topic_l3, negative);
        
        
        
    # dimm led if Lamp 2 is active  
    if ((positive in l2_value) and (negative in lastL2value)):
        D2A.ChangeDutyCycle(20);
        print("l2 Active");
        lastL2value = positive;
        
        
    #l2 and l3 are disabled
    if ((value == False) and (l2_value == negative)):
        D2A.ChangeDutyCycle(0);
        lastL2value = negative;
        
    time.sleep(0.01);
        
    

          

    
    lastVal = value;
    
    
gpio.cleanup();



    