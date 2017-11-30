
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
    socket.on('lobbystate', function(lobbystate) {
    lobbystate = JSON.parse(lobbystate);
    if(lobbystate == "lobby") {
        document.getElementById('lobby').style.display='block';
        document.getElementById('game').style.display='none';
        document.getElementById('loading').style.display='none';
        document.getElementById('gameover').style.display='none';
    } else if (lobbystate == "game") {
        document.getElementById('lobby').style.display='none';
        document.getElementById('game').style.display='block';
        document.getElementById('loading').style.display='none';
        document.getElementById('gameover').style.display='none';
    } else if (lobbystate == "loading") {
        document.getElementById('lobby').style.display='none';
        document.getElementById('game').style.display='none';
        document.getElementById('loading').style.display='block';
        document.getElementById('gameover').style.display='none';
    } else if (lobbystate == "gameover") {
        document.getElementById('lobby').style.display='none';
        document.getElementById('game').style.display='none';
        document.getElementById('loading').style.display='none';
        document.getElementById('gameover').style.display='block';
    }

    gameState = {};
    lastGameState = {};
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
}, 1000/10);

function setOrientation(event) {
    if(window.DeviceOrientationEvent){

        movement.alpha = event.alpha;
        movement.beta = event.beta;
        movement.gamma = event.gamma;
    }
    else{
        movement.alpha = 0;
        movement.beta = 0;
        movement.gamma = 0;
    }
    

}
function setMotion(event) {
    if(window.DeviceOrientationEvent){

        movement.x = event.acceleration.x;
        movement.y = event.acceleration.y;
        movement.z = event.acceleration.z;        
    }
    else{   
        movement.x = 0;
        movement.y = 0;
        movement.z = 0;    
    }

}
function moveUp() {
    console.log('movedup');
}

function moveDown() {
    console.log('moveddown');
}

window.addEventListener('devicemotion', setMotion , true);
window.addEventListener('deviceorientation', setOrientation , true);


function getData(){
    return document.getElementById()

}




