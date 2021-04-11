# au422_tp3_IPSA

Connect to [RDS](https://app.theconstructsim.com/#/) with your logins.

Go to "My rosjects" and create a new project (Select the ROS Melodic distribution) and run it.



In a terminal, follow the instructions **ONE AFTER THE OTHER** :

```bash
cd ~/catkin_ws/src && git clone https://github.com/JohvanyROB/au422_tp3_IPSA.git
cd ~/catkin_ws && catkin_make && source ~/catkin_ws/devel/setup.bash
roscd au422_tp3/scripts
chmod +x path_planning_rrt.py
```



You can now come back to the project subject.