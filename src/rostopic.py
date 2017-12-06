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

def rostopicFunctions(comando, brew):
	global stop_
	stop_ = False
	global ip_

	ip_ = ipgetter.myip()

	comandoSplit = comando.split(" ")
	if comandoSplit[1] == "list":
		if(len(comandoSplit) < 3):
			ip = ''
		else:
			ip = comandoSplit[2]

		data = {'comandoRos':'rostopic', 'funcao':'rostopicList', 'acao':'enviar', 'topic':'', 'freq':'0', 'ip':ip}
		brew.publish("Publisher", data)
		rospy.logwarn("Comando enviado = "+comando)

	elif comandoSplit[1] == "echo":
		if(len(comandoSplit) < 5):
			ip = ''
		else:
			ip = comandoSplit[4]

		if len(comandoSplit) < 4:
			rospy.logwarn("sintaxe = rostopic echo /topic frequency")
		else:
			data = {'comandoRos':'rostopic', 'funcao':'rostopicEcho', 'acao':'enviar', 'topic':comandoSplit[2][1:], 'freq':comandoSplit[3], 'ip':ip}
			brew.publish("Publisher", data)
			rospy.logwarn("Comando enviado = "+comando)

	elif comandoSplit[1] == "info":
		if(len(comandoSplit) < 4):
			ip = ''
		else:
			ip = comandoSplit[3]

		data = {'comandoRos':'rostopic', 'funcao':'rostopicInfo', 'acao':'enviar', 'topic':comandoSplit[2], 'freq':'0', 'ip':ip}
		brew.publish("Publisher", data)
		rospy.logwarn("Comando enviado = "+comando)

	elif comandoSplit[1] == "stop":
		stop_ = True
		rospy.logwarn("mudou pra true")

	else:
		rospy.logwarn("Sintaxe do comando incorreta")	
	
'''INICIO ROSTOPIC LIST'''
def rostopicList(brew, topic, freq, ip):

	global ip_
	dados = ""

	if(ip == '' or ip == ip_):
		master = rosgraph.masterapi.Master('/rostopic')
		resp = master.getPublishedTopics('/')

		for i in range(0, len(resp)):
			dados += "\n"+resp[i][0]

		data = {'dados':dados, 'title':"Resultados de rostopic list do master "+ip_, 'acao':'receber'}
	else:	
		data = {'dados':dados, 'title':"IP = " +ip+ " e nao corresponde ao solicitado", 'acao':'receber'}

	brew.publish("Publisher", data)
'''FIM ROSTOPIC LIST'''


'''INICIO ROSTOPIC ECHO'''
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

	#dados = resp.data
	while(stop_ == False):
		xml = ros2xml(resp, "")
		data = {'dados':xml, 'title':"Resultados de rostopic echo do master "+ip_, 'acao':'receber'}
		brew_.publish("Publisher", data)
		time.sleep(float(freq_))
		rospy.logwarn("aqui = "+str(stop_))

	rospy.logwarn("saiu do while")

	return


def rostopicEcho(brew, topic, freq, ip):
	global brew_
	brew_ = brew

	global freq_
	global stop_
	global ip_

	freq_ = freq
	stop_ = False
	dados = ""

	if(ip == '' or ip == ip_):
		proc = subprocess.Popen(["rostopic type "+topic], stdout=subprocess.PIPE, shell=True)
		(dados, err) = proc.communicate()

		dado = dados.split("/")
		dado[0] += ".msg"

		mod = __import__(dado[0], fromlist=[dado[1]])

		klass = getattr(mod, dado[1].strip())

		rospy.Subscriber(topic, klass, callback)
	else:
		data = {'dados':dados, 'title':"IP = " +ip+ " e nao corresponde ao solicitado", 'acao':'receber'}
		brew.publish("Publisher", data)
'''FIM ROSTOPIC ECHO'''


'''INICIO ROSTOPIC INFO'''
def rostopicInfo(brew, topic, freq, ip):
	global ip_
	dados = ""

	if(ip == '' or ip == ip_):
		proc = subprocess.Popen(["rostopic info "+topic], stdout=subprocess.PIPE, shell=True)
		(dados, err) = proc.communicate()
		ip = ipgetter.myip()
		data = {'dados':dados, 'title':"Resultado de rostopic info "+topic+ " do master "+ip_, 'acao':'receber'}
	else:
		data = {'dados':dados, 'title':"IP = " +ip_+ " e nao corresponde ao solicitado", 'acao':'receber'}

	brew.publish("Publisher", data)

'''FIM ROSTOPIC INFO'''
