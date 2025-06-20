# final_robot_test_description

##### 安裝此ROS套件
```
cd ~/catkin_ws/src
git clone https://github.com/YunZhen2003/final_robot_test_description.git
cd ~/catkin_ws
catkin_make
```

##### 將機器人spawn到TurtleBot3 House地圖
roslaunch final_robot_test_description spawn_in_house.launch

##### 啟用避障模組
roslaunch final_robot_test_description avoid.launch

##### 使用鍵盤控制機器人
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
