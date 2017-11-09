console.log("socket");



var socket = io.connect('http://130.240.93.75:5050');


socket.on('connect', function() {
    //socket.emit('my event', {data: 'I\'m connected!'});
});

var latency = [];
socket.on('broadcast', function(data) {
    latency.push((new Date().getTime() - data.time));
    if(latency.length > 100) {
        latency.shift();
    }
});

var startPing, stopPing;
function ping() {
    startPing = new Date().getTime();
    socket.emit('ping', {});
}
setInterval(function(){
    ping();
}, 2000);

socket.on('ping', function(data) {
    stopPing = new Date().getTime();
    console.log(stopPing-startPing);
});
