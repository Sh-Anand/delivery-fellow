#!/bin/bash
sudo bash -c 'echo 1 > /sys/module/bluetooth/parameters/disable_ertm'
sudo chmod a+rw /dev/ttyACM0
cd delivery-fellow/Jetson/catkin_ws
source devel/setup.bash
roslaunch delivery_fellow delivery_fellow.launch
