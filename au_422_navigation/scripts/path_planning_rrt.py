#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import PoseStamped, Pose2D
from nav_msgs.srv import GetMap
from nav_msgs.msg import Path
import tf

from sys import exit
import cv2


class RRT:
    def __init__(self, K=0, dq=0):
        """ Attributes """
        self.robot_pose = Pose2D()
        self.path = []
        self.listener = tf.TransformListener()
        #TO DO: add your attributes here.... 

        """ Publishers and Subscribers """
        rospy.Timer(rospy.Duration(secs=0.5), self.poseCb)
        rospy.Subscriber("/move_base_simple/goal", PoseStamped, self.goal_pose_cb)
        self.pathPub = rospy.Publisher("/path", Path, queue_size=1)

        """ Load the map and create the related image"""
        self.getMap()


    # **********************************
    def getMap(self):
        """ Call the static_map service and then get the map """
        print("Waiting for map service to be available...")
        rospy.wait_for_service('/static_map')
        try:
            get_map = rospy.ServiceProxy('/static_map', GetMap)
            self.map = get_map().map
            print("Map received !")
        except rospy.ServiceException as e:
            print(f"Map service call failed: {e}")
            exit()

    
    # **********************************
    def poseCb(self, event):
        """ Get the current position of the robot each 500ms """
        try:
            trans, rot = self.listener.lookupTransform("/map", "/base_footprint", rospy.Time(0))
            self.robot_pose.x = trans[0]
            self.robot_pose.y = trans[1]
            print(f"Robot's pose: {self.robot_pose.x}, {self.robot_pose.y}")
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print(f"Could not transform /base_footprint to /map")


    # **********************************
    def goal_pose_cb(self, msg):
        """ TODO - Get the goal pose """
        #get the goal pose here
        #....

        self.run()


    # **********************************
    def run(self):
        """ TODO - Implement the RRT algorithm """
        pass


    # **********************************
    def publishPath(self):
        """ Send the computed path so that RVIZ displays it """
        """ TODO - Transform the waypoints from pixels coordinates to meters in the map frame """
        msg = Path()
        msg.header.frame_id = "map"
        msg.header.stamp = rospy.Time.now()
        path_RVIZ = []
        for pose_img in self.path:
            pose = PoseStamped()
            #pose.pose.position.x = ....
            #pose.pose.position.y = ...
            path_RVIZ.append(pose)
        msg.poses = path_RVIZ
        self.pathPub.publish(msg)


if __name__ == '__main__':
    """ DO NOT TOUCH """
    rospy.init_node("RRT", anonymous=True)

    rrt = RRT()

    rospy.spin()
