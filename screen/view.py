import eventlet
eventlet.sleep() # DONT REMOVE
eventlet.monkey_patch()

import game
import lobby

from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os, time, json, logging, getpass
from flask_socketio import SocketIO, emit

#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hotsecret!'
socketio = SocketIO(app, engineio_logger=False, ping_timeout=5, ping_interval=1, async_mode="eventlet")

def broadcast(topic, message, namespace=None, room=None):
    socketio.emit(topic, json.dumps(message), namespace=namespace, room=room)

class View(object):

    lobby = None
    game = None
    state = 'lobby'
    playing = False

    def __init__(self):
        self.game = game.Game(self)
        self.lobby = lobby.Lobby(self)

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
        self.broadcast('lobbystate', state, '/screen')
        for sid in self.lobby.getGameQueue():
            self.broadcast('lobbystate', state, '/controller', sid)
        return self.state

    def setGameOver(self):
        self.playing = False

    def getLobby(self):
        return self.lobby

    def getGame(self):
        return self.game

    def getSocketIO(self):
        return socketio

    def checkEnoughPlayers(self):
        if self.lobby.isEnough() and self.playing == False:
            self.playing = True
            socketio.start_background_task(game.play)

    def broadcast(self, topic, message, namespace=None, room=None):
        broadcast(topic, message, namespace, room)

    def startFlask(self):
        if getpass.getuser() == 'hotscreen':
            self.openBrowser('localhost:5050/lobby')
        socketio.run(app, host='0.0.0.0', port=5050)

    def openBrowser(self, url):
        opts = Options()
        opts.binary_location = "/usr/bin/chromium-browser"
        opts.add_argument("disable-infobars")
        #opts.add_argument("--kiosk") # Fullscreen mode
        driver = webdriver.Chrome(chrome_options=opts, executable_path=os.getcwd()+"/chromedriver")
        driver.get(url)

view = View()

from handlers import handlers

app.register_blueprint(handlers)

view.startFlask()
#socketio.start_background_task(startFlask)
