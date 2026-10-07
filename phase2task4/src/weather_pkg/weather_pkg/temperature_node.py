#! /usr/bin/env python3

from sensor_msgs.msg import Temperature
import rclpy
from rclpy.node import Node
import random

class Temp(Node):
    def __init__(self):
        super().__init__("temperature_node")
        self.get_logger().info("Temperature Node started!")
        self.publisher_ = self.create_publisher(Temperature, "temperature", 10)
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = Temperature()
        msg.temperature = random.uniform(15.0, 40.0)
        msg.variance = 0.5                              
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published Temperature: {msg.temperature:.2f} °C")

def main():
    rclpy.init()
    temp_node = Temp()
    rclpy.spin(temp_node)
    temp_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
