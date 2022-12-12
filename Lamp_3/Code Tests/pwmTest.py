import RPi.GPIO as gpio
import time

led = 17;
gpio.setmode(gpio.BCM);
gpio.setup(led, gpio.OUT);

D2A = gpio.PWM(led, 60);
D2A.start(50)

while True:
    for i in range(0, 100, 1):
        D2A.ChangeDutyCycle(i);
        time.sleep(0.05);
        
    for i in range(0, 100, 1):
        D2A.ChangeDutyCycle(100 - i);
        time.sleep(0.05);
