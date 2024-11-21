import os

from ament_index_python.packages import get_package_share_directory,get_package_prefix


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.actions import DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, TextSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='office_mate' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','office_mate_simple.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    #ros2 run twist_mux twist_mux --ros-args --params-file ./src/office_mate/config/twist_mux.yaml -r cmd_vel_out:=diff_cont/cmd_vel_unstamped
    twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
    twist_mux = Node(
            package="twist_mux",
            executable="twist_mux",
            parameters=[twist_mux_params, {'use_sim_time': True}],
            remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
        )
    
    joystick = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','joystick.launch.py'
                )])
    )

    foxglove = IncludeLaunchDescription(
                AnyLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('foxglove_bridge'), 'launch', 'foxglove_bridge_launch.xml')])
             )

    gazebo_params_file = os.path.join(get_package_share_directory(package_name),'config','gazebo_params.yaml')

    # Add this code snippet before launching Gazebo
    # os.environ['GAZEBO_RESOURCE_PATH'] = os.path.join(get_package_share_directory(package_name), 'quadruped') + ":" + os.environ.get('GAZEBO_RESOURCE_PATH', '')


    # pkg_share_path = os.pathsep + os.path.join(get_package_prefix(package_name), 'share')
    # if 'GAZEBO_MODEL_PATH' in os.environ:
    #     os.environ['GAZEBO_MODEL_PATH'] += pkg_share_path
    # else:
    #     os.environ['GAZEBO_MODEL_PATH'] =  pkg_share_path

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', '/robot_description',
                                   '-entity', 'office_mate'],
                        output='screen')




    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    # joint_trajectory_cont_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["joint_trajectory_cont"],
    # )

    forward_position_cont_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["forward_position_cont"],
    )

    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[diff_drive_spawner],
        )
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[joint_broad_spawner],
        )
    )


    # delayed_joint_trajectory_cont_spawner = RegisterEventHandler(
    #     event_handler=OnProcessExit(
    #         target_action=spawn_entity,
    #         on_exit=[joint_trajectory_cont_spawner],
    #     )
    # )

    delayed_forward_position_cont_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[forward_position_cont_spawner],
        )
    )

    # ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/office_mate/config/mapper_params_online_async.yaml use_sim_time:=true

    
    slam_params_file = os.path.join(get_package_share_directory("office_mate"),
                                       'config', 'localizer_params_online_async.yaml')
    start_async_slam_toolbox_node = Node(
        parameters=[
          slam_params_file,
        #   {'use_sim_time': use_sim_time}
        ],
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen')

    # ros2 launch office_mate nav2_navigation_launch.py

    nav2 = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory(package_name),'launch','nav2_navigation_launch.py'
            )])
    )


    # Launch them all!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        rsp,
        joystick, # comment to disable joystick 
        twist_mux,
        gazebo,
        spawn_entity,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner,
        # delayed_joint_trajectory_cont_spawner
        delayed_forward_position_cont_spawner,
        foxglove,
        start_async_slam_toolbox_node,
        nav2
    ])
