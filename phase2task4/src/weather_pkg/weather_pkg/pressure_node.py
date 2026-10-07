#! /usr/bin/env python3

from sensor_msgs.msg import FluidPressure
import rclpy
from rclpy.node import Node
import random

class Pressure(Node):
    def __init__(self):
        super().__init__("pressure_node")
        self.get_logger().info("Pressure Node started!")
        self.publisher_ = self.create_publisher(FluidPressure, "pressure", 10)
        self.create_timer(3.0, self.timer_callback)
        
    def timer_callback(self):
        msg = FluidPressure()
        msg.fluid_pressure = random.uniform(900.0, 1100.0)  
        msg.variance = 1.0                                  
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published Pressure: {msg.fluid_pressure:.2f} hPa")

def main():
    rclpy.init()
    pressure_node = Pressure()
    rclpy.spin(pressure_node)
    pressure_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()