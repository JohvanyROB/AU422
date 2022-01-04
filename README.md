# AU422

Connect to [RDS](https://app.theconstructsim.com/#/){target="_blank"} with your logins.

Go to "My rosjects" and create a new project (Select the ROS **Noetic** distribution) and run it.



Open the web shell and follow the instructions **ONE AFTER THE OTHER** :

```bash
sudo apt update && sudo apt install ros-noetic-slam-karto -y
cd ~/catkin_ws/src && git clone https://github.com/JohvanyROB/AU422.git
cd ~/catkin_ws && catkin_make && source ~/catkin_ws/devel/setup.bash
```



You can now come back to the project subject.
