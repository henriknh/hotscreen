console.log("socket");



var socket = io.connect('http://localhost:5050');


socket.on('connect', function() {
    //socket.emit('my event', {data: 'I\'m connected!'});
});

var latency = [];
socket.on('broadcast', function(data) {
    latency.push((new Date().getTime() - data.time));
    if(latency.length > 100) {
        latency.shift();
    }
});


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function printLatency() {
  await sleep(2000);

  let total = 0;
  for(l of latency) {
      total += l;
  }

  console.log('Latency:', Math.round(total/latency.length),'ms');

  printLatency();
}

printLatency();
