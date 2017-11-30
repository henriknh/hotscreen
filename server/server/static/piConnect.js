
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
    socket.on('lobbystate', function(lobbystate) {
        console.log('lobbystate');
        console.log(lobbystate);
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
    });

    socket.on('queueupdated', function(position) {
        console.log('queueupdated');
        console.log(position);
        setLobby(position);
    });
    socket.on('playerstate', function(playerstate) {
        console.log('playerstate');
        playerstate = JSON.parse(playerstate);
        console.log(playerstate.backgroundcolor);
        console.log(playerstate.space.score);
        setGame(playerstate.space.score , playerstate.backgroundcolor);
    });

}

var movement = {
    alpha: 0,
    beta: 0,
    gamma: 0,
    x: 0,
    y: 0,
    z: 0
};
function sendMovement() {
    if(!socket)
        return;
    socket.emit('movement', JSON.stringify(movement));
}

setInterval(function(){
    sendMovement();
}, 1000/10);

function setOrientation(event) {
    if(window.DeviceOrientationEvent && 'ontouchstart' in window){
        movement.alpha = event.alpha;
        movement.beta = event.beta;
        movement.gamma = event.gamma;
    }
}
function setMotion(event) {
    if(window.DeviceOrientation && 'ontouchstart' in window){
        movement.x = event.acceleration.x;
        movement.y = event.acceleration.y;
        movement.z = event.acceleration.z;
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
    return document.getElementById();
}

function setLobby(position){
    console.log("setlobby");
    document.getElementById("queue").innerHTML = "Your place in queue is: " + (parseInt(position) + 1);
}
function setGame(score, background){
    console.log("set score");
    document.getElementById("body").style.background = background;
    console.log(document.getElementById("body").style.background);
    document.getElementById("score").innerHTML = "Your score is: " + score;
}
