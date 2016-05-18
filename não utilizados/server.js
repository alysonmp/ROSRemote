// when window loads call the setup method

			// Spacebrew Object
			var sb
				, app_name = "Ros Cloud"
				;

			var http = require('http');
			var io = require('socket.io');
			require('./js/jq.js');
			require('./js/sb-1.4.1.js');
			var port = 34815;

			// Start the server at port 8080
			var server = http.createServer(function(req, res){ 
			    // Send HTML headers and message
			    res.writeHead(200,{ 'Content-Type': 'text/html' }); 
			    res.end('<h1>Hello Socket Lover!</h1>');
			});

			server.listen(port);

			// Create a Socket.IO instance, passing it our server
			var socket = io.listen(server);

			// Add a connect listener
			socket.on('connection', function(client){ 
			    console.log('Connection to client established');

			    // Success!  Now listen to messages to be received
			    client.on('message',function(event){ 
				console.log('Received message from client!',event);
			    });

			    client.on('disconnect',function(){
				clearInterval(interval);
				console.log('Server has disconnected');
			    });
			});

			setup();


			/**
			* setup Function that connect to spacebrew and creates a listener for clicks of the submit button.
			*/
			function setup (){
				//var random_id = "0000" + Math.floor(Math.random() * 10000)
					;

				//app_name = app_name + ' ' + random_id.substring(random_id.length-4);

				// setup spacebrew
				sb = new Spacebrew.Client();  // create spacebrew client object

				sb.name(app_name);
				sb.description("This app sends text from an HTML form."); // set the app description

		        // create the spacebrew subscription channels
				sb.addPublish("publisher", "string", "");	// create the publication feed
				sb.addSubscribe("subscriber", "string");		// create the subscription feed

				// configure the publication and subscription feeds
				sb.onStringMessage = onStringMessage;		
				sb.onOpen = onOpen;

				// connect to spacbrew
				sb.connect();  

				// listen to button clicks
				//$("#button").on("mousedown", onMouseDown);
			}

			/**
			 * Function that is called when Spacebrew connection is established
			 */
			function onOpen() {
				var message = "Connected as <strong>" + sb.name() + "</strong>. ";
				if (sb.name() === app_name) {
					message += "<br>You can customize this app's name in the query string by adding <strong>name=your_app_name</strong>."
				}
				$("#name").html( message );
			}

			

			/**
			 * onStringMessage Function that is called whenever new spacebrew string messages are received.
			 *          It accepts two parameters:
			 * @param  {String} name    Holds name of the subscription feed channel
			 * @param  {String} value 	Holds value received from the subscription feed
			 */
			var mensagem;
			function onStringMessage( name, value ){
				console.log("[onBooleanMessage] boolean message received ", value);
				$("#msg_received").text(value); // display the sent message in the browser         
				mensagem = value;
				//alert(mensagem);
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
		  /*var listener = new ROSLIB.Topic({
		    ros : ros,
		    name : '/listener',
		    messageType : 'std_msgs/String'
		  });*/
	    	//listener.subscribe(function(message) {
		    var newString = string;
		    console.log('Received message on ' + listener.name + ': ' + string);
		    //enviaRos(message.data);
		    if (newString !== "") {               // if input box is not blank
			console.log("Sending message " + newString); 
			sb.send("publisher", "string", newString);   // send string to spacebrew
			$("#status").text(newString); // display the sent message in the browser         
		    }
		    //listener.unsubscribe();
		  }
