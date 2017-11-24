var socket = io.connect('ws://localhost:5050/screen');
var socket_c = io.connect('ws://localhost:5050/controller');

socket.on('connect', function() {
    console.log('connect');
});

socket.on('disconnect', function() {
    console.log('disconnect');
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
});

window.onload = function(e){
    canvasResize();
};

window.onresize = function(e) {
    canvasResize();
};

var canvas;
var ctx;
var canvasWidth;
var canvasHeight;
var canvasOffsetX;
var canvasOffsetY;
var objectScaling;
function canvasResize() {
    canvas = document.getElementById("gameBoard");
    ctx = canvas.getContext("2d");
    canvasWidth = window.innerWidth;
    canvasHeight = window.innerHeight;
    ctx.canvas.width  = canvasWidth;
    ctx.canvas.height = canvasHeight;
    canvasOffsetX = canvasWidth*0.25;
    canvasOffsetY = canvasHeight*0.6;
    objectScaling = (canvasWidth+canvasHeight)/2/15;
    console.log('objectScaling', objectScaling);
}

let x = 0;
socket.on('gamestate', function(gameState) {
    gameState = JSON.parse(gameState);
    console.log(gameState);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // background
    ctx.fillStyle=gameState.background.color;
    ctx.fillRect(0,0,canvasWidth,canvasHeight);

    // ground
    gameState.ground.forEach(function(ground) {
        ctx.fillStyle=ground.color;
        ctx.fillRect(objectScaling*ground.x+canvasOffsetX,objectScaling*-ground.y+canvasOffsetY,objectScaling*ground.width,objectScaling*-ground.height);
    });

    // obstacles
    gameState.obstacles.forEach(function(obstacle) {
        ctx.fillStyle=obstacle.color;
        ctx.fillRect(objectScaling*obstacle.x+canvasOffsetX,objectScaling*-obstacle.y+canvasOffsetY,objectScaling*obstacle.width,objectScaling*-obstacle.height);
    });

    // players
    gameState.players.forEach(function(player) {
        ctx.fillStyle=player.color;
        ctx.fillRect(objectScaling*player.x+canvasOffsetX,objectScaling*-player.y+canvasOffsetY,objectScaling*player.width,objectScaling*-player.height);
    });
});


socket.on('queue_updated', function(queue) {
    let json = JSON.parse(queue);

    let html = '';
    for(let item of json) {
        html += '<p>'+item+'</p>';
    }

    document.getElementById("queue").innerHTML = "There are "+ json.length +" in queue...";
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


socket.on('countdown', function(countdown) {
    if(countdown < 0) {
        document.getElementById("countdown").style.display = 'none';
        return;
    }
    if(countdown == 0) {
        countdown = "Go!";
    }

    document.getElementById("countdown").style.display = 'block';
    document.getElementById("countdown").innerHTML = countdown;
});
