from paho.mqtt.client import Client as MC
from paho.mqtt.enums import CallbackAPIVersion

class BaseMQTTClient:
    
    def __init__(self, address='localhost', port=1883):
        self.client = MC(CallbackAPIVersion.VERSION2)
        self.address = address
        self.port = port

    def connect(self):
        self.client.connect(self.address, self.port)
        self.client.loop_start()

    def publish(self, topic: str, message: str):
        self.client.publish(topic, message)
