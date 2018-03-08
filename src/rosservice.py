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

def rosserviceFunctions(command, brew):
	global stop_
	stop_ = False

	commandSplit = command.split(" ")
	if commandSplit[1] == "list":
		data = {'commandRos':'rosservice', 'function':'rosserviceList', 'action':'send', 'service':'', 'args':''}
		brew.publish("Publisher", data)
		rospy.logwarn("Sent command = "+command)

	elif commandSplit[1] == "args":
		if len(commandSplit) != 3:
			rospy.logwarn("syntax = rosservice args /service")
		else:
			data = {'commandRos':'rosservice', 'function':'rosserviceArgs', 'action':'send', 'service':commandSplit[2], 'args':''}
			brew.publish("Publisher", data)
			rospy.logwarn("Sent command = "+command)

	elif commandSplit[1] == "call":
		if len(commandSplit) < 3:
			rospy.logwarn("syntax = rosservice call /service")
		elif len(commandSplit) == 3:
			data = {'commandRos':'rosservice', 'function':'rosserviceCall', 'action':'send', 'service':commandSplit[2], 'args':''}
			brew.publish("Publisher", data)
			rospy.logwarn("Sent command = "+command)
		else:
			argsSplit = command.split('"')
			data = {'commandRos':'rosservice', 'function':'rosserviceCall', 'action':'send', 'service':commandSplit[2], 'args':argsSplit[1]}
			brew.publish("Publisher", data)
			rospy.logwarn("Sent command = "+command)

	elif commandSplit[1] == "node":
		if len(commandSplit) != 3:
			rospy.logwarn("syntax = rosservice node /service")
		else:
			data = {'commandRos':'rosservice', 'function':'rosserviceNode', 'action':'send', 'service':commandSplit[2], 'args':''}
			brew.publish("Publisher", data)

			rospy.logwarn("Sent command = "+command)

	elif comandoSplit[1] == "type":
		rospy.logwarn(command)
		if len(commandSplit) < 3:
			rospy.logwarn("syntax = rosservice node /service ( | rossrv (show | list | md5 | package | packages))")
		elif len(comandoSplit) == 3:
			data = {'commandRos':'rosservice', 'function':'rosserviceType', 'action':'send', 'service':commandSplit[2], 'args':''}
			brew.publish("Publisher", data)
			rospy.logwarn("Sent command = "+command)
		else:
			argsSplit = command.split('|')
			rospy.logwarn('argssplit = '+argsSplit[1])
			data = {'commandRos':'rosservice', 'function':'rosserviceType', 'action':'send', 'service':commandSplit[2], 'args':argsSplit[1]}
			brew.publish("Publisher", data)
			rospy.logwarn("Sent command = "+command)

	elif commandSplit[1] == "stop":
		stop_ = True

	else:
		rospy.logwarn("Incorrect command syntax")	
	
'''ROSSERVICE LIST START'''
def rosserviceList(brew, service, args):
	proc = subprocess.Popen(["rosservice list"], stdout=subprocess.PIPE, shell=True)

	(datum, err) = proc.communicate()

	data = {'datum':datum, 'title':"Rosservice list results from master "+brew.name, 'action':'receive'}

	brew.publish("Publisher", data)
'''ROSSERVICE LIST END'''


'''ROSSERVICE ARGS START'''
def rosserviceArgs(brew, service, args):
	proc = subprocess.Popen(["rosservice args "+service], stdout=subprocess.PIPE, shell=True)

	(datum, err) = proc.communicate()

	data = {'datum':datum, 'title':"Rosservice args "+service+ " results from master "+brew.name, 'action':'receive'}
	brew.publish("Publisher", data)
'''ROSSERVICE ARGS END'''


'''ROSSERVICE CALL START'''
def rosserviceCall(brew, service, args):
	proc = subprocess.Popen(["rosservice call "+service+" '"+args+"'"], stdout=subprocess.PIPE, shell=True)
	(dados, err) = proc.communicate()

	data = {'datum':datum, 'title':"Rosservice call "+service+" "+args+ " results from master "+brew.name, 'action':'receive'}
	brew.publish("Publisher", data)
'''ROSSERVICE CALL END'''


'''ROSSERVICE NODE START'''
def rosserviceNode(brew, service, args):
	proc = subprocess.Popen(["rosservice node "+service], stdout=subprocess.PIPE, shell=True)
	(datum, err) = proc.communicate()

	data = {'datum':datum, 'title':"Rosservice node "+service+ " results from master "+brew.name, 'action':'receive'}

	brew.publish("Publisher", data)
'''ROSSERVICE NODE END'''


'''ROSSERVICE TYPE START'''
def rosserviceType(brew, service, args):
	if args=="":
		proc = subprocess.Popen(["rosservice type "+service], stdout=subprocess.PIPE, shell=True)
	else:
		proc = subprocess.Popen(["rosservice type "+service +" | "+ args], stdout=subprocess.PIPE, shell=True)

	(datum, err) = proc.communicate()

	data = {'datum':datum, 'title':"Rosservice type "+service+ " results from master "+brew.name, 'action':'receive'}
	brew.publish("Publisher", data)
'''ROSSERVICE TYPE END'''







