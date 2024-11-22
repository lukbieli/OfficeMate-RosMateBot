import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

import xacro


def generate_launch_description():


    package_name='office_mate' #<--- CHANGE ME

    # Robot State Publisher
    robot_state_publisher_node = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','office_mate_simple.launch.py'
                )]), launch_arguments={'use_sim_time': 'false', 'use_ros2_control': 'true'}.items()
    )
    
    package_name='ldlidar_node' #<--- CHANGE ME
    
    lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
       	     get_package_share_directory(package_name),'launch','ldlidar_with_mgr.launch.py'
                )])
    )

    rpi_params = Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            parameters=["0", "0", "0.15", "0", "0", "0", "base_link", "ldlidar_base"]
        )

    # Launch!
    return LaunchDescription([
        robot_state_publisher_node,
        lidar,
        rpi_params
    ])