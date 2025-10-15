from time import sleep
from random import random
from RobotGui.core.comm.base_client import BaseMQTTClient
from PySide6.QtGui import QKeyEvent, Qt
import threading

mqtt_client = BaseMQTTClient()
mqtt_client.connect()

motion_subscriber = BaseMQTTClient()
motion_subscriber.connect()

def motion_callback(client, userdata, message):
        x, y = map(float, message.payload.decode().split(","))

motion_subscriber.client.message_callback_add("robot/motion", motion_callback)
motion_subscriber.client.subscribe("robot/motion")

def publish_coordinates():
        while True:
            sleep(1)
            x = random()
            y = random()
            mqtt_client.publish("robot/coordinates", f"{x},{y}")
           


