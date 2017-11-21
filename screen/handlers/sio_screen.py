
from view import socketio

from flask import request
from flask_socketio import emit, join_room, leave_room


@socketio.on('ping', namespace='/screen')
def on_ping(message):
    emit('ping', message, namespace='/screen')
