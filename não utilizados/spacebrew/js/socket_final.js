"use strict";

var webSocketsServerPort = 1337;

var webSocketServer = require('websocket').server;
var http = require('http');

var history = [ ];
var clients = [ ];

function htmlEntities(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;')
		      .replace(/"/g, '&quot;');
}

var server = http.createServer(function(request, response) {
});
server.listen(webSocketsServerPort, function() {
    console.log((new Date()) + " Server is listening on port " + webSocketsServerPort);
});

var wsServer = new webSocketServer({
    httpServer: server
});

wsServer.on('request', function(request) {
    console.log((new Date()) + ' Connection from origin ' + request.origin + '.');

    var connection = request.accept(null, request.origin); 

    var index = clients.push(connection) - 1;
    var userName = false;

    console.log((new Date()) + ' Connection accepted.');

    if (history.length > 0) {
	connection.sendUTF(JSON.stringify( { type: 'history', data: history} ));
    }


    connection.on('message', function(message) {
	if (message.type === 'utf8') { // accept only text
	    if (userName === false) { // first message sent by user is their name
		//enviaRos(message);
		console.log(message);
	    } else { // log and broadcast the message
		console.log((new Date()) + ' Received Message from '
		            + userName + ': ' + message.utf8Data);
		
		var obj = {
		    time: (new Date()).getTime(),
		    text: htmlEntities(message.utf8Data),
		    author: userName
		};
		history.push(obj);
		history = history.slice(-100);

		var json = JSON.stringify({ type:'message', data: obj });
		for (var i=0; i < clients.length; i++) {
		    clients[i].sendUTF(json);
		}
	    }
	}
    });

    connection.on('close', function(connection) {
	if (userName !== false) {
	    console.log((new Date()) + " Peer "
		+ connection.remoteAddress + " disconnected.");
	    clients.splice(index, 1);
	}
    });

});
