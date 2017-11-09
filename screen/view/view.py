from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from threading import Thread
import os, time, psutil, json
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hotsecret!'
socketio = SocketIO(app, engineio_logger=False, ping_interval=0.005)

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

class View(object):

    def __init__(self):
        super(View, self).__init__()

        Thread(target = self.startFlask, args = ()).start()

        #self.openBrowser('localhost:5050/lobby')

    def exit(self):
        pass

    def emit(self, topic, message):
        socketio.emit(topic, message)

    def startFlask(self):
        #app.run(host="0.0.0.0", port=5050)
        socketio.run(app, host='0.0.0.0', port=5050)


    def openBrowser(self, url):
        opts = Options()
        opts.binary_location = "/usr/bin/google-chrome-stable"
        opts.add_argument("disable-infobars")
        #opts.add_argument("--kiosk") # Fullscreen mode
        driver = webdriver.Chrome(chrome_options=opts, executable_path=os.getcwd()+"/chromedriver")
        driver.get(url)
