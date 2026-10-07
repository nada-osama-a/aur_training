#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import tty
import termios

class Turtle(Node):
    def __init__(self):
        super().__init__('turtle')
        self.get_logger().info("Turtle Node started!")
        self.pub1 = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pub2 = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        self.get_logger().info("Use Arrow keys to move turtle1 and WASD to move turtle2. Press 'q' to quit.")   
    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
        return key

    def run(self):
        while True:
            key = self.get_key()     
            t1, t2 = Twist(), Twist()  

            if key == '\x1b[A':
                t1.linear.x = 2.0   # Up
            elif key == '\x1b[B': 
                t1.linear.x = -2.0  # Down
            elif key == '\x1b[C':
                t1.angular.z = -2.0 # Right turn
            elif key == '\x1b[D':
                t1.angular.z = 2.0  # Left turn

            elif key == 'w':
                t2.linear.x = 2.0 # Up
            elif key == 's':
                t2.linear.x = -2.0 # Down
            elif key == 'a': 
                t2.angular.z = 2.0 # Left turn
            elif key == 'd': 
                t2.angular.z = -2.0 # Right turn
            elif key == 'q':
                self.get_logger().info("Quitting...")
                break
            self.pub1.publish(t1)
            self.pub2.publish(t2)

def main():
    rclpy.init()
    node =   Turtle()
    node.run()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
