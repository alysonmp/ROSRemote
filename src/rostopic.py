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

def rostopicFunctions(comando, brew):
	global stop_
	stop_ = False

	comandoSplit = comando.split(" ")
	if comandoSplit[1] == "list":
		data = {'comandoRos':'rostopic', 'funcao':'rostopicList', 'acao':'enviar', 'topic':''}
		brew.publish("Publisher", data)
		rospy.logwarn("Comando enviado = "+comando)

	elif comandoSplit[1] == "echo":
		if len(comandoSplit) != 4:
			rospy.logwarn("sintaxe = rostopic echo /topic frequency")
		else:
			data = {'comandoRos':'rostopic', 'funcao':'rostopicEcho', 'acao':'enviar', 'topic':comandoSplit[2][1:]}
			brew.publish("Publisher", data)
			rospy.logwarn("Comando enviado = "+comando)

	elif comandoSplit[1] == "info":
		data = {'comandoRos':'rostopic', 'funcao':'rostopicInfo', 'acao':'enviar', 'topic':comandoSplit[2]}
		brew.publish("Publisher", data)
		rospy.logwarn("Comando enviado = "+comando)

	elif comandoSplit[1] == "stop":
		stop_ = True

	else:
		rospy.logwarn("Sintaxe do comando incorreta")	
	
'''INICIO ROSTOPIC LIST'''
def rostopicList(brew, topic):
	master = rosgraph.masterapi.Master('/rostopic')
	resp = master.getPublishedTopics('/')

	dados = ""
	for i in range(0, len(resp)):
		dados += "\n"+resp[i][0]

	data= {'dados':dados, 'title':"Resultados de rostopic list", 'acao':'receber'}
	brew.publish("Publisher", data)
'''FIM ROSTOPIC LIST'''


'''INICIO ROSTOPIC ECHO'''
def callback(resp):

	global brew_
	global stop_

	stop_ = False

	dados = resp.data
	rospy.logwarn(stop_)
	while(stop_ == False):
		data= {'dados':dados, 'title':"Resultados de rostopic echo ", 'acao':'receber'}
		brew_.publish("Publisher", data)
		time.sleep(1)
		rospy.logwarn("aqui = "+str(stop_))

	rospy.logwarn(stop_)

def rostopicEcho(brew, topic):
	global brew_
	brew_ = brew

	rospy.Subscriber(topic, String, callback)
'''FIM ROSTOPIC ECHO'''


'''INICIO ROSTOPIC INFO'''
def rostopicInfo(brew, topic):
	proc = subprocess.Popen(["rostopic info "+topic], stdout=subprocess.PIPE, shell=True)
	(dados, err) = proc.communicate()
	data = {'dados':dados, 'title':'Resultado de rostopic info '+topic, 'acao':'receber'}
	brew.publish("Publisher", data)

'''FIM ROSTOPIC INFO'''
