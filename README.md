# OfficeMate-RosMateBot
Repository for package containing OfficeMate robot description and launch files


# Setup steps
1. Install ROS2 Humble following steps in URL: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html
   Small tip: execute line to automaticaly source ros when terminal is being opened:
   ```
   echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
   ```
2. Install dependencies:
  ```
  sudo apt install ros-humble-gazebo-ros-pkgs
  sudo apt install ros-humble-xacro ros-humble-joint-state-publisher-gui
  sudo apt install ros-humble-ament-lint-auto
  sudo apt install ros-humble-ros2-control ros-humble-ros2-controllers ros-humble-gazebo-ros2-control
  ```  
3. Prepare workspace
  ```
  mkdir -p dev_ws_office_mate/src
  cd dev_ws_office_mate/src
  ```
4. Clone repository
  ```
  git clone <link_to_repo> 
  ```
5. Rename folder to office_mate (**Important!**)
  ```
  mv OfficeMate-RosMateBot office_mate
  cd ..
  ```
6. If not already installed install colcon
  ```
  sudo apt install python3-colcon-common-extensions
  ```
7. Build package with colcon
  ```
  colcon build --symlink-install
  ```
# Launching package
## High detail model
To launch high detailed model exported from onshape: 
**Warning:** It can cause errors during launch or lag in simulation. Especially if used world is also large
```
source install/setup.bash
ros2 launch office_mate sim.launch.py
```
To use prepared world use argument modifier
```
source install/setup.bash
ros2 launch office_mate sim.launch.py world:=<path_to_world_file>
```
To use LTTS kitchen 3D scan as a model, before calling a launch command change directory to _officemate/gazebo_ where the jpg with textures is located. (That the only way (for now) to make textures visible in gazebo.
```
source install/setup.bash
cd src/office_mate/gazebo
ros2 launch office_mate sim.launch.py world:=<path_to_world_file>
```

## Simple model
To workaround issues with lagging simulation or errors simplified model is available:
```
source install/setup.bash
ros2 launch office_mate sim_simple.launch.py
```
Launch with model of a kitchen
```
source install/setup.bash
cd src/office_mate/gazebo
ros2 launch office_mate sim_simple.launch.py world:=<path_to_world_file>
```

# Steering robot with keyboard
First possibility to steer the model manually is via teleopt_twist_keyboard package
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
```

# Steering robot with foglove joistick
Second one possibility to steer the model manually is via joistick from foxglove.
## Downlad needed software
First you need a foxglove studio app. The debian package is avalaible in website:
```
https://foxglove.dev/download
```
Download it and follow the instrucions there or here.
Do in location where you downlad it:
```
sudo apt install ./foxglove-studio-*.deb
sudo apt update && sudo apt install foxglove-studio
```
Now you need a websocket to connect joystick with ros2.
Download it:
```
sudo apt install ros-humble-foxglove-bridge
```

## Run the applications
Anytime you will run foxglove you will need a connection bridge to communicate it with ROS. Do:
```
ros2 launch foxglove_bridge foxglove_bridge_launch.xml
```
Open foglove studio app. On the left side are Open Data Sources. Click on Open conection..
Then chose Foxglove WebSocket, WebSocket URL left with default settings and click open.
Now click on the user in top right corner and chose "Extensions". Find the Joystick extension and install it.
In the Joystick panel change Data source from "Subscribed Joy Topic" to "Interactive". Change Publish to on and In display section - display value to Custom Display.
Now you need a toystic node and translation node to x, z axes. Run:
```
ros2 launch office_mate joystick.launch.py
```
Now you can steere a robot with joystick.

# Starting Rviz
There is a lunch file for starting rviz
```
source install/setup.bash
ros2 launch office_mate start_rviz.launch.py

```
