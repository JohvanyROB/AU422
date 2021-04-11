#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import rospy
import cv2
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped
from nav_msgs.srv import GetMap
from nav_msgs.msg import Path
from sys import exit


class RRT:
    def __init__(self, K=0, dq=0):
        """ Constructor """
        rospy.Subscriber("/initialpose", PoseWithCovarianceStamped, self.starting_pose_cb)
        rospy.Subscriber("/move_base_simple/goal", PoseStamped, self.goal_pose_cb)
        self.pathPub = rospy.Publisher("/path", Path, queue_size=1)

        print("Waiting for map service to be available...")
        rospy.wait_for_service('/static_map')   #The node waits for the service that provides the map to be avaiblable
        try:    #GET the map data
            get_map = rospy.ServiceProxy('/static_map', GetMap)
            self.map = get_map().map
            print("Map received !")
        except rospy.ServiceException as e:
            print("Map service call failed: %s"%e)
            exit()

        """ TODO - Add your attributes """
        self.starting_pose_received = False
        self.path = []


    # **********************************
    def starting_pose_cb(self, msg):
        """ TODO - Get the starting pose """
        self.starting_pose_received = True


    # **********************************
    def goal_pose_cb(self, msg):
        """ TODO - Get the goal pose """
        #get the goal pose here
        #....

        #TO DOT TOUCH
        if self.starting_pose_received:
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
