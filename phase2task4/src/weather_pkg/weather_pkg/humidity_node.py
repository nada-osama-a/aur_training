#! /usr/bin/env python3

from sensor_msgs.msg import RelativeHumidity
import rclpy
from rclpy.node import Node
import random

class Humidity(Node):
    def __init__(self):
        super().__init__("humidity_node")
        self.get_logger().info("Humidity Node started!")
        self.publisher_ = self.create_publisher(RelativeHumidity, "humidity", 10)
        self.create_timer(2.0, self.timer_callback)
        
    def timer_callback(self):
        msg = RelativeHumidity()
        msg.relative_humidity = random.uniform(20, 100)
        msg.variance = 0.05                                  
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published Humidity: {msg.relative_humidity:.2f} %")
 
def main():
    rclpy.init()
    humidity_node = Humidity()
    rclpy.spin(humidity_node)
    humidity_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()