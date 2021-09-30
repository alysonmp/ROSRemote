#!/usr/bin/env python3

import termios
import tty
import time
import json
import sys
import threading
import subprocess
from roscommands import rosCommandsFunctions
import roscommands
from rosrun import rosrunFunctions
import rosrun
from rosservice import rosserviceFunctions
import rosservice
from rostopic import rostopicFunctions
import rostopic
import rosgraph.masterapi
from pySpacebrew.spacebrew import Spacebrew
from std_msgs.msg import String
from cloud_ros.srv import Comando
import rospy
import roslib
roslib.load_manifest('cloud_ros')


def send(req):
    global brew

    comando = req.comando.split(" ")

    if(comando[0] == "rostopic"):
        rostopicFunctions(req.comando, brew)
    elif(comando[0] == "rosservice"):
        rosserviceFunctions(req.comando, brew)
    elif(comando[0] == "rosrun"):
        rosrunFunctions(req.comando, brew)
    elif(comando[0] == "roscommands"):
        rosCommandsFunctions(req.comando, brew)
    else:
        rospy.logwarn("Incorrect command syntax")
    return True


def received(data):
    print("recieving data via the websocket: " + data)
    global brew
    global start_time

    if data['action'] == "send" and data['commandRos'] == 'rostopic':
        method = getattr(rostopic, data['function'])
        result = method(brew, data['topic'], data['freq'], data['ip'])
    elif data['action'] == "send" and data['commandRos'] == 'rosservice':
        method = getattr(rosservice, data['function'])
        result = method(brew, data['service'], data['args'])
    elif data['action'] == "send" and data['commandRos'] == 'rosrun':
        method = getattr(rosrun, data['function'])
        result = method(brew, data['package'],
                        data['executable'], data['parameters'])
    elif data['action'] == "send" and data['commandRos'] == 'roscommands':
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
            # tty.setraw(sys.stdin)
            ch = sys.stdin.read(1)[0]

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

    # server = "localhost"
    server = "forever-spacebrew.herokuapp.com/"

    global brew

    brew = Spacebrew(name=name, server=server)
    brew.addPublisher("ROS_Publisher")
    brew.addPublisher("ROS_Publisher_two", "boolean")
    print('main_cloud_ros: adding publisher')
    brew.addSubscriber("Subscriber", "string")

    try:
        pass
        # start-up spacebrew
        brew.start()
        brew.subscribe("Subscriber", received)

        # thread2 = myThread(1, "Thread-2", 1)
        # thread2.start()
    finally:
        rospy.init_node('cloud_ros_node')
        rospy.loginfo("cloud_ros node is up and running!!!")

    rospy.loginfo('service has been started')
    s = rospy.Service('send_data', Comando, send)
    rospy.spin()

def myhook():
    global thread2
    brew.stop()
    # thread2.raise_exception()
    print ("shutdown time!")


if __name__ == '__main__':
    rospy.on_shutdown(myhook)
    try:
        cloud_ros()
    except rospy.ROSInterruptException:
        pass