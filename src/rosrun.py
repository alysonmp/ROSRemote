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

def rosrunFunctions(comando, brew):
	global stop_
	stop_ = False

	comandoSplit = comando.split(" ")
	rospy.logwarn(comando)
	if len(comandoSplit) == 3:
		data = {'comandoRos':'rosrun', 'funcao':'rosrun', 'acao':'enviar', 'package':comandoSplit[1], 'executable':comandoSplit[2]}
		brew.publish("Publisher", data)
		rospy.logwarn("Comando enviado = "+comando)
	else:
		rospy.logwarn("Sintaxe do comando incorreta")	
	
'''INICIO ROSRUN'''
def rosrun(brew, package, executable):
	proc = subprocess.Popen(["rosrun " +package +" "+ executable], stdout=subprocess.PIPE, shell=True)
	(dados, err) = proc.communicate()
	data = {'dados':dados, 'title':'Resultado de rostopic info '+topic, 'acao':'receber'}
	brew.publish("Publisher", data)
'''FIM ROSRUN'''

