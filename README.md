# OfficeMate-RosMateBot
Rpository for package contiaing OfficeMate robot description and launch files

mkdir dev_ws_office_mate/src
cd dev_ws_office_mate/src
git clone 

mv OfficeMate-RosMateBot office_mate
cd ..
colcon build --symlink-intall
source install/setup.bash
ros2 launch office_mate sim.launch.py
ros2 launch office_mate sim_simple.launch.py