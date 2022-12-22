# system library
import RPi.GPIO as GPIO
from time import sleep
import time
# mqtt library
import paho.mqtt.client as mqtt

# MQTT Daten
username = ""
password = ""
address = "test.mosquitto.org"

topic_lamp1 = "hska/lamp1/position"
topic_lamp2 = "hska/lamp2/position"

# variables
pos2 = False

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# ultrasonic Sensor
GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# setup LED
LEDPIN = 22
duty_cycle = 0
GPIO.setup(LEDPIN, GPIO.OUT)  # Set pin to be an output pin and set initial value to low (off)
LED = GPIO.PWM(LEDPIN, 100)
LED.start(duty_cycle)


def get_distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # time difference between start and arrival
    time_elapsed = stop_time - start_time
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (time_elapsed * 34300) / 2
    print(distance)
    return distance


def fade_LED(target):
    global duty_cycle
    if target > duty_cycle:
        for x in range(duty_cycle, target + 1, 1):
            LED.ChangeDutyCycle(x)
            sleep(0.01)
    else:
        for x in range(duty_cycle, target - 1, -1):
            LED.ChangeDutyCycle(x)
            sleep(0.01)

    duty_cycle = target


# mqtt callback
def on_message(client, userdata, message):
    global pos2
    pos2 = message.payload.decode() == "1"
    print(f"Received pos2 = {pos2}")


if __name__ == "__main__":
    # connect
    client = mqtt.Client()
    client.connect(address, 1883, 60)

    # subscribe to pos2
    client.on_message = on_message
    client.subscribe(topic_lamp2)
    client.loop_start()

    # do ForEVER
    while True:
        pos1 = get_distance() < 100

        if pos1:
            fade_LED(100)  # LED an
            client.publish(topic_lamp1, 1)
        else:
            if pos2:
                fade_LED(10)  # LED halb hell
            else:
                fade_LED(0)  # LED aus
            client.publish(topic_lamp1, 0)

        sleep(0.1)
