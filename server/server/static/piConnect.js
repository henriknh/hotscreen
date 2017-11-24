
var ip = 'ws://' + getIP();
var socket = io.connect(ip);

function getIP() {
    var ip = document.getElementById('ip');
    var port = document.getElementById('port');
    return ip+port;
}


socket.on('connect', function () {
        socket.emit('setup');

});
socket.on('updated', function() {
        console.log('updated and finnished');
});

function sendData(event) {

    var alpha = event.alpha;
    var beta = event.beta;
    var gamma = event.gamma;

    var json1 = JSON.stringify({data: alpha + ':' + beta + ':' + gamma});
    socket.emit('device',json1);


}
function moveUp() {
    console.log('movedup');
    socket.emit('move' , 'up');
}

function moveDown() {
    console.log('moveddown');
    socket.emit('move' , 'down');
}
window.addEventListener('devicemotion', sendData , true);


function getData(){
    return document.getElementById()

}




