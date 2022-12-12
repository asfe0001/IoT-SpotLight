import paho.mqtt.client as mqtt
import time
 
broker_url = "test.mosquitto.org"
broker_port = 1883
 
def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code: {}".format(rc))
 
def on_disconnect(client, userdata, rc):
   print("Client Got Disconnected")
   
def on_message(client, userdata, message):
    print("message")
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)
 
client.subscribe("lampe_test", qos=1)
 
client.publish(topic="test", payload="TestingPayload", qos=1, retain=False)
 
client.loop_start()

while True:
    time.sleep(1)
    
client.loop_stop()