#!/usr/bin/env python

import roslib; roslib.load_manifest('cloud_ros')
import rospy
from cloud_ros.srv import *
from std_msgs.msg import String
from pySpacebrew.spacebrew import Spacebrew
import rosgraph.masterapi

import rostopic 
from rostopic import rostopicFunctions

import rosservice
from rosservice import rosserviceFunctions

import rosrun
from rosrun import rosrunFunctions

import json

def enviar(req):
	global brew

	comando = req.comando.split(" ")

	if(comando[0] == "rostopic"):
		rostopicFunctions(req.comando, brew)
	elif(comando[0] == "rosservice"):
		rosserviceFunctions(req.comando, brew)
	elif(comando[0] == "rosrun"):
		rosrunFunctions(req.comando, brew)
	else:
		rospy.logwarn("Sintaxe do comando incorreta")

def recebido(data):
	global brew

	if data['acao']=="enviar" and data['comandoRos']=='rostopic':
		method = getattr(rostopic, data['funcao'])
		result = method(brew, data['topic'])
	elif data['acao']=="enviar" and data['comandoRos']=='rosservice':
		method = getattr(rosservice, data['funcao'])
		result = method(brew, data['service'], data['args'])
	elif data['acao']=="enviar" and data['comandoRos']=='rosrun':
		method = getattr(rosrun, data['funcao'])
		result = method(brew, data['package'], data['executable'])
	else:
		rospy.logwarn(data['title']+"\n"+data['dados'])

def cloud_ros():
	name = "rosPy Example"
	server = "sandbox.spacebrew.cc"
	
	global brew

	brew = Spacebrew(name=name, server=server)
	brew.addPublisher("Publisher")
	brew.addSubscriber("Subscriber")

	try:
		# start-up spacebrew
		brew.start()
		brew.subscribe("Subscriber", recebido)
	finally: 
		rospy.init_node('cloud_ros_node')
		rospy.loginfo("cloud_ros node is up and running!!!")

	s = rospy.Service('send_data', Comando, enviar)

	rospy.spin()

if __name__ == '__main__':
	cloud_ros()

