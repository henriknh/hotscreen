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
    } else if (lobbystate == "game") {
        document.getElementById('lobby').style.display='none';
        document.getElementById('game').style.display='block';
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
function canvasResize() {
    console.log(window.innerWidth);
    console.log(window.innerHeight);
    canvas = document.getElementById("gameBoard");
    ctx = canvas.getContext("2d");
    ctx.canvas.width  = window.innerWidth;
    ctx.canvas.height = window.innerHeight;
}

let x = 0;
socket.on('gamestate', function(state) {
    console.log(state);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if(x > 50)
        x = 0;
    x += 1;
    ctx.fillRect(x,50,150,100);
    ctx.fillRect(x*2,200,150,100);
    ctx.fillRect(x*3,350,150,100);
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


socket.on('preplay_countdown', function(countdown) {
    if(countdown == 0) {
        countdown = "Go!";
    }
    document.getElementById("countdown").innerHTML = countdown;
});
