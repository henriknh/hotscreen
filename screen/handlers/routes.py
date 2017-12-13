import json
from flask import Flask, render_template, redirect
from . import handlers
from view import view

#reg = Registration()
#port = 5050
#reg.register(port)

@handlers.route("/")
def index():
    return render_template('index.html', qr=view.getRegistration().qr, connect_code=view.getRegistration().code, ws_port=view.getPort())

@handlers.route("/heartbeat")
def heartbeat():
    return "ok"
