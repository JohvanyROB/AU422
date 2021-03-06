#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy

from geometry_msgs.msg import Pose2D, Twist
from nav_msgs.msg import Path
import tf

class Agent:
    def __init__(self):
        self.listener = tf.TransformListener()

        self.robot_pose = Pose2D()
        self.goal_received, self.reached = False, False

        self.path_sub = rospy.Subscriber("path", Path, self.plannerCb, queue_size=1)
        self.vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        self.timer_pose = rospy.Timer(rospy.Duration(0.5), self.poseCb)
        self.timer_follower = rospy.Timer(rospy.Duration(0.1), self.moveToGoal)


    def poseCb(self, event):
        """ Get the current position of the robot each 500ms """
        try:
            trans, rot = self.listener.lookupTransform("/map", "/base_footprint", rospy.Time(0))
            self.robot_pose.x = trans[0]
            self.robot_pose.y = trans[1]
            self.robot_pose.theta = tf.transformations.euler_from_quaternion(rot)[2]
            print(f"Robot's pose: {self.robot_pose.x:.2f}, {self.robot_pose.y:.2f}, {self.robot_pose.theta:.2f}")
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print(f"Could not transform /base_footprint to /map")


    def plannerCb(self, msg):
        self.reached, self.goal_received = False, True
        self.path = msg.poses[1:]   #remove the robot's pose


    def moveToGoal(self, event):
        if not self.reached and self.goal_received:
            pass
            #Add your strategy here

    
    def send_velocities(self):
        self.linear = self.constraint(self.linear, min=-2.0, max=2.0)
        self.angular = self.constraint(self.angular)

        cmd_vel = Twist()
        cmd_vel.linear.x = self.linear
        cmd_vel.angular.z = self.angular
        self.vel_pub.publish(cmd_vel)


    def constraint(self, val, min=-1.0, max=1.0):
        if val < min:
            return min
        elif val > max:
            return max
        return val
    

if __name__ == "__main__":
    rospy.init_node("agent_node", anonymous=True)    

    node = Agent()

    rospy.spin()