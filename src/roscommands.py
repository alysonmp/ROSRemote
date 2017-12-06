#!/usr/bin/env python

import roslib; roslib.load_manifest('cloud_ros')
import rospy
from cloud_ros.srv import *
from pySpacebrew.spacebrew import Spacebrew
from std_msgs.msg import String
import rosgraph.masterapi
import time
import os
import subprocess
import threading
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

def rosCommandsFunctions(command, brew):

	#implementar rospack list "nome"

	commandSplit = command.split(" ")
	if len(commandSplit) == 1:
		data = {'commandRos':'roscommands', 'function':'roscommands', 'action':'send', 'commands':commandSplit[0]}
		brew.publish("Publisher", data)
		rospy.logwarn("command enviado = "+command)
	elif (commandSplit[1] == "set_robot"):
		data = {'commandRos':'roscommands', 'function':'set_robot', 'action':'send', 'commands':commandSplit[2]}
		brew.publish("Publisher", data)
		rospy.logwarn("Sent command = "+command)
	else:
		rospy.logwarn("Wrong command syntax")	
	
'''INICIO ROSCOMMANDS'''
def set_robot(brew, commands):
	global robot 
	robot = commands

def roscommands(brew, commands):
	global robot
	rospy.logwarn(robot)

	speed = Twist()
	global proc
	if(commands == "up"): 
		speed.linear.x = 2
		speed.linear.y = 0
		speed.linear.z = 0

		speed.angular.x = 0
		speed.angular.y = 0
		speed.angular.z = 0
	elif(commands == "down"):
		speed.linear.x = -2
		speed.linear.y = 0
		speed.linear.z = 0

		speed.angular.x = 0
		speed.angular.y = 0
		speed.angular.z = 0
	elif(commands == "right"):
		speed.linear.x = 0
		speed.linear.y = 0
		speed.linear.z = 0

		speed.angular.x = 0
		speed.angular.y = 0
		speed.angular.z = -2
	elif(commands == "left"):
		speed.linear.x = 0
		speed.linear.y = 0
		speed.linear.z = 0

		speed.angular.x = 0
		speed.angular.y = 0
		speed.angular.z = 2

	robots = robot.split(":")

	for rob in robots:
		pub = rospy.Publisher(rob+'/cmd_speed', Twist, queue_size=10)
		pub.publish(speed)

		speed.linear.x = 0
		speed.linear.y = 0
		speed.linear.z = 0

		speed.angular.x = 0
		speed.angular.y = 0
		speed.angular.z = 0
	
		time.sleep(0.5)

		pub = rospy.Publisher(rob+'/cmd_speed', Twist, queue_size=10)
		pub.publish(speed)

'''FIM ROSCOMMANDS'''


