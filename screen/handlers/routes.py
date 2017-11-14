import psutil, json
from flask import Flask, render_template, redirect
from . import handlers
from view import view

@handlers.route("/")
def index():
    return render_template('index.html', qr="qr code", connect_code="1234")

@handlers.route("/status")
def status():
    data = {
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().percent
    }
    return json.dumps(data)
