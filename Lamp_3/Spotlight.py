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
topic_l3 = "lampe3/zustand2";
topic_l2 ="lampe_test";

l2_value = "NULL";

#mqtt callback
def on_connect_c(client, userdata, flags, rc):
    print("Connected");

    
def on_message_c(client, userdata, message):
    print(message.payload.decode());
    l2_value = message.payload.decode();

#pin setup

gpio.setmode(gpio.BCM);

gpio.setup(sensor, gpio.IN);
gpio.setup(led, gpio.OUT);


#mqtt setup
client = mqtt.Client("Lamp3");
client.on_connect = on_connect_c;
client.on_message = on_message_c;
client.connect(address);

client.subscribe(topic_l2);
client.subscribe(topic_l3);

value = 0;
lastVal = value;
 
 
#int sensor
value = gpio.input(sensor);
client.publish(topic_l3, not value);

client.loop_start();


while(1):
    value = not (gpio.input(sensor));
     
    
    #publish and led update
    if (lastVal != value):
        gpio.output(led, value);
        client.publish(topic_l3, value);
        
        
    if (l2_value is "True"):
        
        
    time.sleep(0.01);
        
    

          


    lastVal = value;
    
    
gpio.cleanup();
