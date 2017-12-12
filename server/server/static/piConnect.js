
var ip;
var port;
var socket;
console.log(ip);

function setIP(ipIn ,portIn) {
    ip = ipIn;
    port = portIn;
    socketUIConnect();
}

function socketUIConnect() {
    console.log('socketUIConnect');
    console.log(ip);
    console.log(port);

    socket = io.connect('ws://' + ip + ':' + port + '/controller', {'forceNew': true});

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
            setGameOver();
            socket.disconnect();
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
        console.log(playerstate);

        var board = document.getElementById("game");
        board.innerHTML = "";
        while (board.firstChild) {
            board.removeChild(board.firstChild);
        }
        
        if(playerstate.hasOwnProperty('space')){
            console.log('space');
            console.log(playerstate.space);
            setSpaceGame(playerstate);    
        }
        else if(playerstate.hasOwnProperty('quiz')){
            console.log('quiz');
            console.log(playerstate.quiz);

            setQuizGame(playerstate);
        }    
        
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
}, 1000/30);

function setOrientation(event) {
    if(window.DeviceOrientationEvent && 'ontouchstart' in window){
        movement.alpha = event.alpha;
        movement.beta = event.beta;
        movement.gamma = event.gamma;
    }
}
function setMotion(event) {
    if(window.DeviceOrientationEvent && 'ontouchstart' in window){
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
    document.getElementById("lobby").innerHTML = "Place in queue: " + (parseInt(position) + 1);
}
function setSpaceGame(state){

    var board = document.getElementById("game");
    board.style.backgroundColor = state.backgroundcolor;

    var score = document.createElement('div');
    score.className = 'score';
    score.innerHTML = state.space.score;
    board.appendChild(score);

    //document.getElementById("score").innerHTML = "Your score is: " + state.space.score;
}
function setQuizGame(state){


    var board = document.getElementById("game");
    board.style.backgroundColor = state.backgroundcolor;

    var progress = document.createElement('div');
    progress.className = 'progress';
    progress.innerHTML = 'Question '+(state.quiz.questionnumber+1) + ' of ' + state.quiz.totalquestions;
    board.appendChild(progress);

    if(state.quiz.hasOwnProperty('correctanswer')){
        var table = document.createElement('table');

        state.quiz.answers.forEach(function(answer, index){

            var tr = document.createElement('tr');

            var td = document.createElement('td');
            td.innerHTML = answer;
            if(state.quiz.correctanswer == index && state.quiz.selected == index) {
                td.className = 'selected correct';
            } else if(state.quiz.correctanswer == index) {
                td.className = 'correct';
            } else if(state.quiz.selected == index) {
                td.className = 'selected wrong';
            }
            tr.appendChild(td);

            table.appendChild(tr);

        });
        
        board.appendChild(table);
    }   
    else{
        var table = document.createElement('table');

        state.quiz.answers.forEach(function(answer, index){

            var tr = document.createElement('tr');

            var td = document.createElement('td');
            td.innerHTML = answer;
            if(state.quiz.selected == index) {
                td.className = 'selected';
            }
            tr.appendChild(td);

            table.appendChild(tr);

        });
        
        board.appendChild(table);

    }
    
}
function setGameOver() {
    var board = document.getElementById("gameover");

    var gameover = document.createElement('h1');
    gameover.className = 'title';
    gameover.innerHTML = "Game Over";
    board.appendChild(gameover);

    var button = document.createElement('button');
    button.className = 'button';
    button.innerHTML = "Play again!"
    board.appendChild(button);
    button.onclick = function(){
        board.removeChild(gameover);
        board.removeChild(button);
        socketUIConnect();
    }
    
}