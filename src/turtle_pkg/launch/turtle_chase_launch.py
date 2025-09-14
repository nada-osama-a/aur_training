from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('turtle_pkg')
    config = os.path.join(pkg_share, 'config', 'turtle_params.yaml')

    ld = LaunchDescription()

    demo_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='sim',
        parameters=[config]
    )
    turtle_chase_node = Node(
        package='turtle_pkg',
        executable='turtle_chase',
        name='turtle_chase',
        parameters=[config]
    )

    ld.add_action(demo_node)
    ld.add_action(turtle_chase_node)
    return ld
