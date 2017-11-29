
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

    /*var alpha = event.accelerator.zIndex;
    var beta = event.beta;
    var gamma = event.gamma;
    let test = {x: 0, y: 0, z:0, rotation};
    var json1 = JSON.stringify({data: alpha + ':' + beta + ':' + gamma});*/
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
    movement.x = 0;
    movement.y = 0;
    movement.z = 0;
}
function moveUp() {
    console.log('movedup');
    socket.emit('move' , 'up');
}

function moveDown() {
    console.log('moveddown');
    socket.emit('move' , 'down');
}
//window.addEventListener('devicemotion', setOrientation , true);
window.addEventListener('deviceorientation', setOrientation , true);


function getData(){
    return document.getElementById()

}




