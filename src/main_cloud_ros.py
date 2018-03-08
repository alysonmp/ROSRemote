#!/usr/bin/env python

import roslib; roslib.load_manifest('cloud_ros')
import rospy
from cloud_ros.srv import Comando
from std_msgs.msg import String
from pySpacebrew.spacebrew import Spacebrew
import rosgraph.masterapi

import rostopic 
from rostopic import rostopicFunctions

import rosservice
from rosservice import rosserviceFunctions

import rosrun
from rosrun import rosrunFunctions

import roscommands
from roscommands import rosCommandsFunctions

import subprocess
import threading

import sys, tty, termios

import json
import time

def send(req):
	
	global brew

	comando = req.command.split(" ")

	if(comando[0] == "rostopic"):
		rostopicFunctions(req.command, brew)
	elif(comando[0] == "rosservice"):
		rosserviceFunctions(req.command, brew)
	elif(comando[0] == "rosrun"):
		rosrunFunctions(req.command, brew)
	elif(comando[0] == "roscommands"):
		rosCommandsFunctions(req.command, brew)
	else:
		rospy.logwarn("Incorrect command syntax")

def received(data):
	global brew
	global start_time

	if data['action']=="send" and data['commandRos']=='rostopic':
		method = getattr(rostopic, data['function'])
		result = method(brew, data['topic'], data['freq'], data['ip'])
	elif data['action']=="send" and data['commandRos']=='rosservice':
		method = getattr(rosservice, data['function'])
		result = method(brew, data['service'], data['args'])
	elif data['action']=="send" and data['commandRos']=='rosrun':
		method = getattr(rosrun, data['function'])
		result = method(brew, data['package'], data['executable'], data['parameters'])
	elif data['action']=="send" and data['commandRos']=='roscommands':
		method = getattr(roscommands, data['function'])
		result = method(brew, data['commands'])
	else:
		rospy.logwarn(data['title']+"\n"+data['datum'])

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
	
	global brew

	while(True):
		orig_settings = termios.tcgetattr(sys.stdin)
		tty.setcbreak(sys.stdin)
		#tty.setraw(sys.stdin)
		ch=sys.stdin.read(1)[0]

		if(ch == 'A'):
			comm = "up"
		elif(ch == 'B'):
			comm = "down"
		elif(ch == 'C'):
			comm = "right"
		elif(ch == 'D'):
			comm = "left"
		else:
			comm = ""

		if(comm != ""):
			rosCommandsFunctions(comm, brew)

def cloud_ros():
	name = "rosPy Example"

	server = "localhost"
	#server = "sandbox.spacebrew.cc"
	
	global brew

	brew = Spacebrew(name=name, server=server)
	brew.addPublisher("Publisher")
	brew.addSubscriber("Subscriber")

	try:
		# start-up spacebrew
		brew.start()
		brew.subscribe("Subscriber", received)

		thread2 = myThread(1, "Thread-2", 1)
		thread2.start()
	finally: 
		rospy.init_node('cloud_ros_node')
		rospy.loginfo("cloud_ros node is up and running!!!")

	s = rospy.Service('send_data', Comando, send)

	rospy.spin()

if __name__ == '__main__':
	cloud_ros()

