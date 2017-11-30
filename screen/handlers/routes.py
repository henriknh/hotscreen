import json
from flask import Flask, render_template, redirect
from . import handlers
from view import view
from registration import *

reg = Registration()
port = 5050
reg.register(port)

@handlers.route("/")
def index():
    return render_template('index.html', qr=reg.qr, connect_code=reg.code)

@handlers.route("/heartbeat")
def heartbeat():
    return
