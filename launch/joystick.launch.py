from launch import LaunchDescription
from launch_ros.actions import Node

import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    joy_params = os.path.join(get_package_share_directory('office_mate'),'config','joystick.yaml')

    joy_node = Node(
            package='joy',
            executable='joy_node',
            parameters=[joy_params],
         )
    
    teleop_node = Node(
            package='teleop_twist_joy', 
            executable='teleop_node',
            name = 'teleop_node',
            parameters=[joy_params],
            remappings=[('/cmd_vel', '/cmd_vel_joy')]
            # remappings=[('/cmd_vel', 'diff_cont/cmd_vel_unstamped')]
            )

    joy_teleop = Node(
        package='joy_teleop', 
        executable='joy_teleop',
        name='joy_teleop',
        parameters=[joy_params]
    )

    return LaunchDescription([
        joy_node,
        teleop_node,
        joy_teleop
    ])