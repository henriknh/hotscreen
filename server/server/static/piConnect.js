
var ip = "";
var socket;
console.log(ip);





function setIP(ip ,port) {
    ip = 'ws://' + ip + ':' + port + '/controller';
    console.log(ip);

    socket = io.connect(ip);

    socket.on('connect', function () {
        socket.emit('setup');
    });
    socket.on('disconnect', function () {
        console.log('Disconect');
    });
    socket.on('updated', function() {
            console.log('updated and finnished');
    });
}

var movement = {};
function sendMovement() {
    if(!socket)
        return;

    console.log(movement);
    socket.emit('movement', JSON.stringify(movement));
}

setInterval(function(){
    sendMovement();
}, 1000/3);

function setOrientation(event) {
    movement.alpha = event.alpha;
    movement.beta = event.beta;
    movement.gamma = event.gamma;

}
function setMotion(event) {
    movement.x = event.acceleration.x;
    movement.y = event.acceleration.y;
    movement.z = event.acceleration.z;
}
function moveUp() {
    console.log('movedup');
    movement.up = 1;
}

function moveDown() {
    console.log('moveddown');
    movement.down = 1;
}
window.addEventListener('devicemotion', setMotion , true);
window.addEventListener('deviceorientation', setOrientation , true);


function getData(){
    return document.getElementById()

}




