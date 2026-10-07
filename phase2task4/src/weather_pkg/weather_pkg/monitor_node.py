#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Temperature, RelativeHumidity, FluidPressure

class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')
        self.get_logger().info("Monitor Node started!")

        self.temperature = None
        self.relative_humidity = None
        self.fluid_pressure = None
        self.counter = 0

        self.temp_sub = self.create_subscription(Temperature, 'temperature', self.temp_callback, 10)
        self.hum_sub = self.create_subscription(RelativeHumidity, 'humidity', self.hum_callback, 10)
        self.pres_sub = self.create_subscription(FluidPressure, 'pressure', self.pres_callback, 10)

        self.file = open("weather_readings.txt", "a",buffering=1)

        self.create_timer(1.0, self.print_readings)

    def temp_callback(self, msg: Temperature):
        self.temperature = msg.temperature

    def hum_callback(self, msg: RelativeHumidity):
        self.relative_humidity = msg.relative_humidity

    def pres_callback(self, msg: FluidPressure):
        self.fluid_pressure = msg.fluid_pressure

    def print_readings(self):
        if self.temperature is None or self.relative_humidity is None or self.fluid_pressure is None:
            return 

        self.counter += 1
        output = (f"[{self.counter}] "
                  f"Temp = {self.temperature:.2f} °C, "
                  f"Humidity = {self.relative_humidity:.2f} %, "
                  f"Pressure = {self.fluid_pressure:.2f} hPa")
        
        self.get_logger().info(output)
        self.file.write(output + "\n")

def main():
    rclpy.init()
    node = MonitorNode()
    rclpy.spin(node)
    node.file.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
