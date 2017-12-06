#!/usr/bin/env python

import roslib; roslib.load_manifest('cloud_ros')
import rospy
from cloud_ros.srv import *
from pySpacebrew.spacebrew import Spacebrew
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import rosgraph.masterapi
import time
import os
import subprocess

import ipgetter
import importlib

#from rosgraph_msgs.msg import Log
from geometry_msgs.msg import Twist

#import std_msgs.msg
#import geometry_msgs.msg
#import rosgraph_msgs.msg

def rostopicFunctions(command, brew):
	global stop_
	stop_ = False
	global ip_

	ip_ = ipgetter.myip()

	commandSplit = command.split(" ")
	if commandSplit[1] == "list":
		if(len(commandSplit) < 3):
			ip = ''
		else:
			ip = commandSplit[2]

		data = {'commandRos':'rostopic', 'function':'rostopicList', 'action':'send', 'topic':'', 'freq':'0', 'ip':ip}
		brew.publish("Publisher", data)
		rospy.logwarn("sent command = "+command)

	elif commandSplit[1] == "echo":
		if(len(commandSplit) < 5):
			ip = ''
		else:
			ip = commandSplit[4]

		if len(commandSplit) < 4:
			rospy.logwarn("syntax = rostopic echo /topic frequency")
		else:
			data = {'commandRos':'rostopic', 'function':'rostopicEcho', 'action':'send', 'topic':commandSplit[2][1:], 'freq':commandSplit[3], 'ip':ip}
			brew.publish("Publisher", data)
			rospy.logwarn("sent command = "+command)

	elif commandSplit[1] == "info":
		if(len(commandSplit) < 4):
			ip = ''
		else:
			ip = commandSplit[3]

		data = {'commandRos':'rostopic', 'function':'rostopicInfo', 'action':'send', 'topic':commandSplit[2], 'freq':'0', 'ip':ip}
		brew.publish("Publisher", data)
		rospy.logwarn("sent command = "+command)

	elif commandSplit[1] == "stop":
		stop_ = True

	else:
		rospy.logwarn("Wrong command syntax")	
	
'''ROSTOPIC LIST START'''
def rostopicList(brew, topic, freq, ip):

	global ip_
	datum = ""

	if(ip == '' or ip == ip_):
		master = rosgraph.masterapi.Master('/rostopic')
		resp = master.getPublishedTopics('/')

		for i in range(0, len(resp)):
			datum += "\n"+resp[i][0]

		data = {'datum':datum, 'title':"Rostopic list results from master "+ip_, 'action':'receive'}
	else:	
		data = {'datum':datum, 'title':"IP = " +ip+ " does not correspond to the requested", 'action':'receive'}

	brew.publish("Publisher", data)
'''ROSTOPIC LIST END'''


'''ROSTOPIC ECHO START'''
def ros2xml(msg, name, depth=0):
	xml = "";
	tabs = "\t"*depth

	if hasattr(msg, "_type"):
	    type = msg._type
	    xml = xml + tabs + "<" + name + " type=\"" + type + "\">\n"

	    try:
		for slot in msg.__slots__:
		    xml = xml + ros2xml(getattr(msg, slot), slot, depth=depth+1)
	    except:
		xml = xml + tabs + str(msg)
	    xml = xml + tabs + "</" + name + ">\n"
	else:
	    xml = xml + tabs + "<" + name + ">" + str(msg) + "</" + name + ">\n"
	return xml

def callback(resp):

	global brew_
	global stop_
	global freq_
	global ip_

	#datum = resp.data
	while(stop_ == False):
		xml = ros2xml(resp, "")
		data = {'datum':xml, 'title':"Rostopic echo results from master "+ip_, 'action':'receive'}

		brew_.publish("Publisher", data)
		time.sleep(float(freq_))
		#rospy.logwarn("aqui = "+str(stop_))

	return


def rostopicEcho(brew, topic, freq, ip):
	global brew_
	brew_ = brew

	global freq_
	global stop_
	global ip_

	freq_ = freq
	stop_ = False
	datum = ""

	if(ip == '' or ip == ip_):
		proc = subprocess.Popen(["rostopic type "+topic], stdout=subprocess.PIPE, shell=True)
		(datum, err) = proc.communicate()

		data = datum.split("/")
		data[0] += ".msg"

		mod = __import__(data[0], fromlist=[data[1]])

		klass = getattr(mod, data[1].strip())

		rospy.Subscriber(topic, klass, callback)
	else:
		data = {'datum':datum, 'title':"IP = " +ip+ " does not correspond to the requested", 'action':'receive'}
		brew.publish("Publisher", data)
'''FIM ROSTOPIC ECHO'''


'''ROSTOPIC INFO START'''
def rostopicInfo(brew, topic, freq, ip):
	global ip_
	datum = ""

	if(ip == '' or ip == ip_):
		proc = subprocess.Popen(["rostopic info "+topic], stdout=subprocess.PIPE, shell=True)
		(datum, err) = proc.communicate()
		ip = ipgetter.myip()
		data = {'datum':datum, 'title':"Rostopic info results "+topic+ " from master "+ip_, 'action':'receive'}
	else:
		data = {'datum':datum, 'title':"IP = " +ip_+ " does not correspond to the requested", 'action':'receive'}

	brew.publish("Publisher", data)

'''ROSTOPIC INFO END'''
