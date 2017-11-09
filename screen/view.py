from game import *
from lobby import *

from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os, time, psutil, json, logging
from flask_socketio import SocketIO, emit
from gevent import monkey, sleep

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hotsecret!'
socketio = SocketIO(app, engineio_logger=False, ping_timeout=5, ping_interval=1, async_mode="eventlet")

@app.route("/")
def index():
    return "Hello World!"

@app.route("/lobby")
def lobby():
    return render_template('lobby.html', qr="qr code", connect_code="1234")

@app.route("/play")
def play():
    socketio.emit('qweasd', {'data': 42, 'time':time.time()*1000})
    return render_template('play.html', name="name_play")

@app.route("/status")
def status():
    data = {
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory(),
        'network': psutil.net_io_counters(pernic=True),
        'temperature': psutil.sensors_temperatures(),
        'fans': psutil.sensors_fans()
    }
    return json.dumps(data)

@socketio.on('my event')
def test_message(message):
    print(message)
    emit('my response', {'data': 'got it!'})

@socketio.on('ping')
def test_message(message):
    emit('ping', message)

@socketio.on('connect')
def on_connect():
    print('%s connected' % request.sid)
    view.getLobby().connectToLobby(request.sid)
    broadcast('queue_updated', view.getLobby().getLobbyQueue())

@socketio.on('disconnect')
def on_disconnect():
    print('%s disconnected' % request.sid)
    view.getLobby().disconnectFromLobby(request.sid)
    broadcast('queue_updated', view.getLobby().getLobbyQueue())

def broadcast(topic, message):
    socketio.emit(topic, json.dumps(message))


class View(object):

    lobby = None
    game = None

    def __init__(self):
        #self.openBrowser('localhost:5050/lobby')

        self.game = Game(self)
        self.lobby = Lobby(self)

    def getLobby(self):
        return self.lobby

    def getGame(self):
        return self.game

    def emit(self, topic, message):
        broadcast(topic, message)

    def startFlask(self):
        socketio.run(app, host='0.0.0.0', port=5050)

    def openBrowser(self, url):
        opts = Options()
        opts.binary_location = "/usr/bin/google-chrome-stable"
        opts.add_argument("disable-infobars")
        #opts.add_argument("--kiosk") # Fullscreen mode
        driver = webdriver.Chrome(chrome_options=opts, executable_path=os.getcwd()+"/chromedriver")
        driver.get(url)

    def sleep(self, time):
        sleep(1)



def startFlask():
    socketio.run(app, host='0.0.0.0', port=5050)

view = View()
view.startFlask()
#socketio.start_background_task(startFlask)
