import psutil, json
from flask import Flask, render_template, redirect
from . import handlers
from view import view
from registration import *

reg = Registration()
port = 5000
reg.register(port)

@handlers.route("/")
def index():
    return render_template('index.html', qr=reg.qr, connect_code=reg.code)

@handlers.route("/status")
def status():
    data = {
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().percent
    }
    return json.dumps(data)
