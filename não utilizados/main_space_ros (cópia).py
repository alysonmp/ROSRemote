#!/usr/bin/env python

import roslib; roslib.load_manifest('space_ros')
import rospy
from space_ros.srv import *
from std_msgs.msg import String
import json
from StringIO import StringIO
from bond import make_bond
from django.shortcuts import render_to_response
try:
    from django.utils import simplejson as json
except:
    import simplejson as json
 
def enviar(req):
	settings.configure()
	js_data = json.dumps("rostopic list")
	render_to_response("spacebrew/index.html", {"my_data": js_data})

	#php = make_bond('PHP')

	#php.eval_block('''echo "<script type='text/javascript' src='spacebrew/js/jq.js'></script>";''')
	#php.eval_block('''echo "<script type='text/javascript' src='spacebrew/js/sb-1.4.1.js'></script>";''')
	#php.eval_block('''echo "<script type='text/javascript' src='http://cdn.robotwebtools.org/EventEmitter2/current/eventemitter2.min.js'></script>";''')
	#php.eval_block('''echo "<script type='text/javascript' src='http://cdn.robotwebtools.org/roslibjs/current/roslib.min.js'></script>";''')

	#js = make_bond('JavaScript', def_args=False)
	#js.eval_block('function enviaRos() { echo "rostopic list; }')
	#js.export(enviaRos)

	'''js.eval_block(
		var sb
			, app_name = "Ros Cloud"
			;

		function setup (){
			sb = new Spacebrew.Client();  // create spacebrew client object

			sb.name(app_name);
			sb.description("This app sends text from an HTML form."); // set the app description

			sb.addPublish("publisher", "string", "");	// create the publication feed
			sb.addSubscribe("subscriber", "string");		// create the subscription feed

			sb.onStringMessage = onStringMessage;		
			sb.onOpen = onOpen;

			sb.connect();  
		}

		function onOpen() {
			var message = "Connected as <strong>" + sb.name() + "</strong>. ";
			if (sb.name() === app_name) {
				message += "<br>You can customize this app's name in the query string by adding <strong>name=your_app_name</strong>."
			}
			$("#name").html( message );
		}

		var mensagem;
		function onStringMessage( name, value ){
			console.log("[onBooleanMessage] boolean message received ", value);
			$("#msg_received").text(value); // display the sent message in the browser         
			mensagem = value;
			var string = new ROSLIB.Topic({
			    ros : ros,
			    name : '/resposta',
			    messageType : 'std_msgs/String'
			  });

			  var msg = new ROSLIB.Message({
			    data : JSON.stringify(mensagem)
			  });

			  string.publish(msg);
		}

		var ros = new ROSLIB.Ros({
		    url : 'ws://localhost:9090'
		  });

		  ros.on('connection', function() {
		    console.log('Connected to websocket server.');
		  });

		  ros.on('error', function(error) {
		    console.log('Error connecting to websocket server: ', error);
		  });

		  ros.on('close', function() {
		    console.log('Connection to websocket server closed.');
		  });

	    	function enviaRos(string){
		    var newString = string;
		    if (newString !== "") {               // if input box is not blank
			sb.send("publisher", "string", newString);   // send string to spacebrew
			$("#status").text(newString); // display the sent message in the browser         
		    }
		  })    
	rospy.logwarn("passou")    
	enviaRos = js.eval('setup()')
	rospy.logwarn("passou2")
	enviaRos = js.eval('enviaRos()')
	rospy.logwarn("passou2")
	val = enviaRos2("rostopic list")'''

	rospy.logwarn("passou2")
	#val = js.call('enviaRos', "rostopic list")

	#print val

def space_ros():
	rospy.init_node('space_ros_node')
	rospy.loginfo("space_ros node is up and running!!!")

	s = rospy.Service('send_data', Comando, enviar)

	rospy.spin()

if __name__ == '__main__':
	space_ros()

