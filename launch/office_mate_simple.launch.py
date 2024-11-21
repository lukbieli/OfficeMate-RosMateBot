import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_ros2_control = LaunchConfiguration('use_ros2_control')

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('office_mate'))
    xacro_file = os.path.join(pkg_path,'description_simple','robot.urdf.xacro')
    # robot_description_config = xacro.process_file(xacro_file).toxml()
    robot_description_config = Command(['xacro ', xacro_file, ' use_ros2_control:=', use_ros2_control, ' sim_mode:=', use_sim_time])
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time}

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        # emulate_tty=True,
        # parameters=[{'use_sim_time': True, 'robot_description': Command(['xacro ', xacro_file])}],
        parameters = [params],
        output="screen"
    )


    # Launch!
    return LaunchDescription([
        robot_state_publisher_node
    ])
