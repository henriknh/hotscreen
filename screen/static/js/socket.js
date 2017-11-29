var socket = io.connect('ws://localhost:5050/screen');
var socket_c = io.connect('ws://localhost:5050/controller');

socket.on('connect', function() {
    console.log('connect');
});

socket.on('disconnect', function() {
    console.log('disconnect');
});

socket.on('lobbystate', function(lobbystate) {
    console.log(typeof lobbystate);
    lobbystate = JSON.parse(lobbystate);

    console.log(lobbystate);
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

window.onload = function(e){
    canvasResize();
    mainLoop();
    renderLoop();
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
}

var gameState = {};
var lastGameState = {};
var gameStateTick = 0;

socket.on('gamestate', function(gameStateIn) {
    gameStateTick = window.performance.now();
    lastGameState = gameState;
    gameState = JSON.parse(gameStateIn);
});

var fps = 60;
var ticks = 0;
var lastTick = 0;
function mainLoop()
{
    // Do stuff...

    //window.setTimeout(mainLoop, 1000 / fps);
}
function renderLoop() {
    //ticks++;

    let nowTick = window.performance.now();
    let deltaTime = nowTick - lastTick;
    lastTick = nowTick;

    if(typeof gameState !== 'undefined' && typeof lastGameState !== 'undefined') {
        if(Object.keys(gameState).length !== 0 && gameState.constructor === Object && Object.keys(lastGameState).length !== 0 && lastGameState.constructor === Object) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            let timeSinceLastGameStatus = (window.performance.now() - gameStateTick)/ 1000;
            deltaTimeGameState = gameState.timestamp - lastGameState.timestamp;
            let deltaXGameState = gameState.players[0].x - lastGameState.players[0].x;
            let deltaXPerSecond = deltaXGameState / deltaTimeGameState;
            let deltaX = deltaXPerSecond * timeSinceLastGameStatus;

            ctx.fillStyle=gameState.players[0].color;
            ctx.fillRect(objectScaling*(gameState.players[0].x+deltaX),objectScaling*-0+canvasOffsetY,objectScaling*gameState.players[0].width,objectScaling*-gameState.players[0].height);


        }
    }



    //ctx.clearRect(0, 0, canvas.width, canvas.height);

    /*// background
    if(gameState.hasOwnProperty('background')) {
        ctx.fillStyle=gameState.background.color;
        //ctx.fillRect(0,0,canvasWidth,canvasHeight);
    }

    // ground
    if(gameState.hasOwnProperty('ground')) {
        gameState.ground.forEach(function(ground) {
            ctx.fillStyle=ground.color;
            //ctx.fillRect(objectScaling*ground.x+canvasOffsetX,objectScaling*-ground.y+canvasOffsetY,objectScaling*ground.width,objectScaling*-ground.height);
        });
    }

    // obstacles
    if(gameState.hasOwnProperty('obstacles')) {
        gameState.obstacles.forEach(function(obstacle) {
            ctx.fillStyle=obstacle.color;
            ctx.fillRect(xPosition+canvasOffsetX,-obstacle.y+canvasOffsetY,objectScaling*obstacle.width,objectScaling*-obstacle.height);
            //ctx.fillRect(obstacle.x,objectScaling*-obstacle.y+canvasOffsetY,objectScaling*obstacle.width,objectScaling*-obstacle.height);
        });
    }

    // players
    if(gameState.hasOwnProperty('players')) {
        gameState.players.forEach(function(player) {
            ctx.fillStyle=player.color;
            ctx.fillRect(objectScaling*player.x+canvasOffsetX,objectScaling*-player.y+canvasOffsetY,objectScaling*player.width,objectScaling*-player.height);
        });
    }*/

	//window.requestAnimationFrame(renderLoop);
	window.setTimeout(renderLoop, 1000 / fps);
}

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
    startPing = window.performance.now();
    socket.emit('ping', {});
}

setInterval(function(){
    ping();
}, 1000);

socket.on('ping', function(data) {
    stopPing = window.performance.now();
    console.log((stopPing-startPing).toFixed(2)+ ' ms\n#'+ticks+' render updates');
    ticks = 0;
});


socket.on('countdown', function(countdown) {
    console.log(countdown);
    if(countdown < 0) {
        document.getElementById("countdown").style.display = 'none';
        return;
    }
    if(countdown == 0) {
        countdown = "Go!";
        setTimeout(function(){
            document.getElementById("countdown").style.display = 'none';
        }, 1000);
    }

    document.getElementById("countdown").style.display = 'block';
    document.getElementById("countdown").innerHTML = countdown;
});
