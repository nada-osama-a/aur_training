#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
import random
import math

class TurtleChase(Node):
    def __init__(self):
        super().__init__('turtle_chase')

        self.declare_parameter("collision_distance")
        self.collision_distance = self.get_parameter("collision_distance").get_parameter_value().double_value

        self.enemy_positions = {}
        self.name = {}

        self.score = 0
        self.score_pub = self.create_publisher(Int32, '/score', 10)

        self.player_pose = None
        self.create_subscription(Pose, '/turtle1/pose', self.player_callback, 10)

        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.kill_client = self.create_client(Kill, '/kill')

        for i in range(1, 4):
            name = f'enemy{i}'
            self.spawn_enemy(name)

        self.create_timer(0.1, self.check_collisions)
        self.create_timer(0.5, self.move_enemies)

        self.get_logger().info('Turtle Chase Game Started!')

    def player_callback(self, msg):
        self.player_pose = msg

    def enemy_callback(self, name):
        def callback(msg):
            self.enemy_positions[name] = msg
        return callback

    def spawn_enemy(self, name):
        x = random.uniform(1.0, 10.0)
        y = random.uniform(1.0, 10.0)

        req = Spawn.Request()
        req.x = x
        req.y = y
        req.theta = 0.0
        req.name = name

        future = self.spawn_client.call_async(req)

        def callback(fut):
            spawned_name = fut.result().name
            self.get_logger().info(f'Spawned {spawned_name} at ({x:.2f}, {y:.2f})')
            self.create_subscription(Pose, f'/{spawned_name}/pose', self.enemy_callback(spawned_name), 10)
            self.name[spawned_name] = self.create_publisher(Twist, f'/{spawned_name}/cmd_vel', 10)

        future.add_done_callback(callback)

    def kill_and_respawn(self, name):
        req = Kill.Request()
        req.name = name
        future = self.kill_client.call_async(req)

        def callback(fut):
            self.get_logger().info(f'Killed {name}, respawning...')
            if name in self.name:
                del self.name[name]
            self.spawn_enemy(name)

        future.add_done_callback(callback)

    def find_distance(self, pose1, pose2):
        return math.sqrt((pose1.x - pose2.x)**2 + (pose1.y - pose2.y)**2)

    def check_collisions(self):
        if self.player_pose is None:
            return
        for name, pose in list(self.enemy_positions.items()):
            if self.find_distance(self.player_pose, pose) < self.collision_distance:
                self.get_logger().info(f'{name} was hit!')
                self.kill_and_respawn(name)
                self.score += 1
                score_msg = Int32()
                score_msg.data = self.score
                self.score_pub.publish(score_msg)
                self.get_logger().info(f'Your Score: {self.score}')

    def move_enemies(self):
        for name, pub in self.name.items():
            twist = Twist()
            twist.linear.x = random.uniform(0.5, 2.0)
            twist.angular.z = random.uniform(-2.0, 2.0)
            pub.publish(twist)

def main():
    rclpy.init()
    node = TurtleChase()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
