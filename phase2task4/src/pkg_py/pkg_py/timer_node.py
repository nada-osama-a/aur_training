#! /usr/bin/env python3

import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__("timer_node")
        self.get_logger().info("Timer Started !")
        self.counter=10
        self.create_timer(1,self.timer_callback)

    def timer_callback(self):
        if self.counter<0:
            self.get_logger().info("Time is up!")
            self.destroy_node()
            return
        else:
            self.get_logger().info(f" {self.counter}")
            self.counter-=1

def main():
    rclpy.init()
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()