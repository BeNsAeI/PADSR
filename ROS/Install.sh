#!/bin/bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
sudo apt-get update
echo "Pick the package to install:"
echo "1. Desktop-Full Install: (Recommended, Default)"
echo "2. Desktop Install"
echo "3. ROS-Base: (Bare Bones)"
echo "4. Individual Package"
read option
if [ $option -eq 1 ]
then
echo "Option selected: Desktop-Full Install"
read -p "Press enter to install"
sudo apt-get install ros-kinetic-desktop-full
fi
if [ $option -eq 2 ]
then
echo "Option selected: Desktop Install"
read -p "Press enter to install"
sudo apt-get install ros-kinetic-desktop
fi
if [ $option -eq 3 ]
then
echo "Option selected: ROS-Base"
read -p "Press enter to install"
sudo apt-get install ros-kinetic-ros-base
fi
if [ $option -eq 4 ]
then
echo "Option selected: Individual Package"
read -p "Press enter to continue"
echo "Listing packages:"
apt-cache search ros-kinetic
echo "____________________________________________________________"
echo "Type in package name:"
read option
read -p "Press enter to install package $option"
sudo apt-get install ros-kinetic-$option
fi
echo "____________________________________________________________"
read -p "Done! Press enter to continue"
