console.log("socket");



var socket = io.connect('ws://130.240.93.75:5050');



function makeid() {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for (var i = 0; i < 5; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));

  return text;
}


socket.on('connect', function() {
    socket.emit('new_player', makeid());
});

socket.on('disconnect', function() {
    console.log('disconnect');
});

socket.on('gamestate', function(data) {
    console.log(data);
});

socket.on('queue_updated', function(queue) {

    let json = JSON.parse(queue);

    let html = '';
    for(let item of json) {
        html += '<p>'+item+'</p>';
    }

    document.getElementById("queue").innerHTML = html;
});

var startPing, stopPing;
function ping() {
    startPing = new Date().getTime();
    socket.emit('ping', {});
}

setInterval(function(){
    ping();
}, 1000);

socket.on('ping', function(data) {
    stopPing = new Date().getTime();
    console.log((stopPing-startPing)+ ' ms');
});
