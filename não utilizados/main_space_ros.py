#!/usr/bin/env python

import roslib; roslib.load_manifest('space_ros')
import rospy
from space_ros.srv import *
from std_msgs.msg import String
import json
from StringIO import StringIO
import websocket
import zerorpc
from websocket import create_connection

def enviar(req):
	#c = zerorpc.Client()
	#c.connect("ws://localhost:9090")
	#print c.hello("RPC")

	global ws

	print "Sending "+req.comando+"..."
	ws.send(req.comando)
	print "Sent"
	print "Receiving..."
	result =  ws.recv()
	print "Received '%s'" % result
	ws.close()


	rospy.logwarn(req.comando)

def space_ros():
	global ws
	ws = websocket.WebSocket()
	ws.connect("ws://localhost:1337/")

	rospy.init_node('space_ros_node')
	rospy.loginfo("space_ros node is up and running!!!")

	s = rospy.Service('send_data', Comando, enviar)

	rospy.spin()

if __name__ == '__main__':
	space_ros()

