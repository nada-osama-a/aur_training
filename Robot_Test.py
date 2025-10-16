import threading
from time import sleep
from random import random
from RobotGui.core.comm.base_client import BaseMQTTClient


mqtt_client = BaseMQTTClient()
mqtt_client.connect()
mqtt_client.client.loop_start()  

motion_subscriber = BaseMQTTClient()
motion_subscriber.connect()
motion_subscriber.client.loop_start()

def motion_callback(client, userdata, message):
    x, y = map(float, message.payload.decode().split(","))
    print(f"Motion received: x={x:.2}, y={y:.2}")

motion_subscriber.client.message_callback_add("robot/motion", motion_callback)
motion_subscriber.client.subscribe("robot/motion")

def publish_coordinates():
    while True:
        sleep(1)
        x = random()
        y = random()
        mqtt_client.publish("robot/coordinates", f"{x:.2},{y:.2}")
        print(f"Published coordinates: {x},{y}")

threading.Thread(target=publish_coordinates, daemon=True).start()

while True:
    sleep(0.1)
