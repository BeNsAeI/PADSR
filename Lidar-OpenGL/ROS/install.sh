## Install ros (Jade) according to this guide: http://wiki.ros.org/jade/Installation/Ubuntu
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://pool.sks-keyservers.net:80 --recv-key 0xB01FA116
sudo apt-get update
sudo apt-get install ros-jade-desktop-full

### init ros
sudo rosdep init
rosdep update
echo "source /opt/ros/jade/setup.bash" >> ~/.bashrc
source ~/.bashrc
sudo apt-get install python-rosinstall

### Create a ROS Workspace
ls
mkdir -p ./catkin_ws/src
cd ~/Projects/PADSR/Lidar-OpenGL/ROS/catkin_ws/src
catkin_init_workspace

### Clone the ROS node for the Lidar in the catkin workspace src dir
git clone https://github.com/robopeak/rplidar_ros.git

### Build with catkin
cd ~/Projects/PADSR/Lidar-OpenGL/ROS/catkin_ws/
catkin_make

### Set environment when build is complete
source devel/setup.bash

### Launch demo with rviz
roslaunch rplidar_ros view_rplidar.launch
