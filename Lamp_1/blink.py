import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
import paho.mqtt.client as mqtt

# MQTT Daten
username=""
password=""
address="test.mosquitto.org"

# connect
client = mqtt.Client()
client.username_pw_set(username, password)
client.connect(address, 1883, 60)

exit()

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
LEDPIN = 22
GPIO.setup(LEDPIN, GPIO.OUT) # Set pin 8 to be an output pin and set initial value to low (off)
LED = GPIO.PWM(LEDPIN, 100)

LED.start(0)

while True: # Run forever
 for x in range(0,100):     
     LED.ChangeDutyCycle(x) # Turn on
     sleep(0.01)
     
 for x in range(0,100):     
     LED.ChangeDutyCycle(100 - x) # Turn on
     sleep(0.01)
         
     
 #sleep(1) # Sleep for 1 second
 #LED.ChangeDutyCycle(50) # Turn off
 #sleep(1) # Sleeangp for 1 second