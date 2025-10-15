from paho.mqtt.enums import CallbackAPIVersion
import paho.mqtt.subscribe as subscribe

from RobotGui.core.comm.base_client import BaseMQTTClient
import RobotGui.core.comm.sub.coords as coords


class CoordinatesClient(BaseMQTTClient):

    def __init__(self, address='localhost', port=1883):
        super().__init__(address, port)
        self.client.on_connect = self._on_connect

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print('Failed to connect . Retrying...')
        else:
            subscribe.callback(coords.callback, 'robot/coordinates')

    def setup(self, coords_slot):
        coords.slot = coords_slot
        self.connect()
