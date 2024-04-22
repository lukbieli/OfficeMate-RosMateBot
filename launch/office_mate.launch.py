import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node

# this is the function launch  system will look for
def generate_launch_description():

    ####### DATA INPUT ##########
    urdf_file = 'robot.urdf'
    #xacro_file = "urdfbot.xacro"
    package_name = "office_mate"

    ####### DATA INPUT END ##########
    print("Fetching URDF ==>")

    pkg_path = os.path.join(get_package_share_directory(package_name))
    xacro_file = os.path.join(pkg_path,'description','robot.urdf.xacro')
    # xacro_file = os.path.join(pkg_path,'quadruped','robot.urdf')

    # robot_desc_path = os.path.join(get_package_share_directory(package_description), "quadruped", urdf_file)
    # robot_description_config = Command(['xacro ', xacro_file])

    # Robot State Publisher

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        # emulate_tty=True,
        parameters=[{'use_sim_time': True, 'robot_description': Command(['xacro ', xacro_file])}],
        output="screen"
    )


    # create and return launch description object
    return LaunchDescription(
        [            
            robot_state_publisher_node,
        ]
    )