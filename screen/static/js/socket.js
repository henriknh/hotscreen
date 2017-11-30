var socket = io.connect('ws://localhost:5050/screen');
//var socket_c = io.connect('ws://localhost:5050/controller');

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

    gameState = {};
    lastGameState = {};
});

window.onload = function(e){
    canvasResize();
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
    objectScaling = (canvasWidth+canvasHeight)/2/100;
}

var gameState = {};
var lastGameState = {};
var gameStateTick = 0;

socket.on('gamestate', function(gameStateIn) {
    gameStateTick = window.performance.now();
    lastGameState = gameState;
    gameState = JSON.parse(gameStateIn);
});

var fps = 30;
var ticks = 0;
var lastTick = 0;

function renderLoop() {
    ticks++;

    let nowTick = window.performance.now();
    let deltaTime = nowTick - lastTick;
    lastTick = nowTick;

    if(typeof gameState !== 'undefined' && typeof lastGameState !== 'undefined') {
        if(Object.keys(gameState).length !== 0 && gameState.constructor === Object && Object.keys(lastGameState).length !== 0 && lastGameState.constructor === Object) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            let timeSinceLastGameStatus = (window.performance.now() - gameStateTick)/ 1000;
            deltaTimeGameState = gameState.timestamp - lastGameState.timestamp;

            // Background
            if(gameState.hasOwnProperty('background')) {
                ctx.fillStyle=gameState.background.color;
                ctx.fillRect(0,0,canvasWidth,canvasHeight);
            }

            // Players
            if(gameState.hasOwnProperty('players')) {
                gameState.players.forEach(function (player, index) {
                    if(lastGameState.players[index] && !player.dead) {
                        let pos = calcObjectPostion(gameState.players[index], lastGameState.players[index], deltaTimeGameState, timeSinceLastGameStatus);
                        drawSpaceship(pos, gameState.players[index]);
                    }
                });
            }

            // Obstacles
            if(gameState.hasOwnProperty('asteroids')) {
                gameState.asteroids.forEach(function (asteroid, index) {
                    if(lastGameState.asteroids[index] && !asteroid.dead) {
                        let pos = calcObjectPostion(gameState.asteroids[index], lastGameState.asteroids[index], deltaTimeGameState, timeSinceLastGameStatus);
                        drawAsteroid(pos, gameState.asteroids[index]);
                    }
                });
            }

            // Stars
            if(gameState.hasOwnProperty('stars')) {
                gameState.stars.forEach(function (obstacle, index) {
                    if(lastGameState.stars[index] && !obstacle.dead) {
                        let pos = calcObjectPostion(gameState.stars[index], lastGameState.stars[index], deltaTimeGameState, timeSinceLastGameStatus);
                        drawStars(pos, gameState.stars[index]);
                    }
                });
            }
        }
    }

	//window.requestAnimationFrame(renderLoop);
	window.setTimeout(renderLoop, 1000 / fps);
}

function calcObjectPostion(state1, state2, deltaTimeGameState, timeSinceLastGameStatus) {
    let deltaXGameState = state1.x - state2.x;
    let deltaXPerSecond = deltaXGameState / deltaTimeGameState;
    let deltaX = deltaXPerSecond * timeSinceLastGameStatus;

    let deltaYGameState = state1.y - state2.y;
    let deltaYPerSecond = deltaYGameState / deltaTimeGameState;
    let deltaY = deltaYPerSecond * timeSinceLastGameStatus;

    return {x: (state1.x+deltaX)*canvasWidth*0.01, y: (state1.y+deltaY)*canvasHeight*0.01};
}

function drawSpaceship(pos, state) {
    ctx.fillStyle=state.color;
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
    ctx.lineTo(pos.x-canvasWidth*0.01*state.width/2, pos.y+canvasHeight*0.01*state.height);
    ctx.lineTo(pos.x+canvasWidth*0.01*state.width/2, pos.y+canvasHeight*0.01*state.height);
    ctx.fill();
}

function drawAsteroid(pos, state) {
    ctx.fillStyle=state.color;
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
    ctx.lineTo(pos.x-canvasWidth*0.01*state.width/2, pos.y+canvasHeight*0.01*state.height/2);
    ctx.lineTo(pos.x, pos.y+canvasHeight*0.01*state.height);
    ctx.lineTo(pos.x+canvasWidth*0.01*state.width/2, pos.y+canvasHeight*0.01*state.height/2);
    ctx.fill();
}

function drawStars(pos, state) {
    ctx.fillStyle=state.color;
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y-canvasHeight*0.01*state.height/2);
    ctx.lineTo(pos.x-canvasWidth*0.01*state.width/2, pos.y);
    ctx.lineTo(pos.x, pos.y+canvasHeight*0.01*state.height/2);
    ctx.lineTo(pos.x+canvasWidth*0.01*state.width/2, pos.y);
    ctx.fill();
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

/*function movement() {
    socket_c.emit('movement', {x: 0, y: 0, z: 0, alpha: 0, beta: Math.sin(window.performance.now()*0.001)*50*-1, gamma: 0});
}
setInterval(function(){
    movement();
}, 1000/10);

socket_c.on('playerstate', function(playerState) {
    console.log(playerState);
});*/
