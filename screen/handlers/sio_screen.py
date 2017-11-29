
from view import socketio, view, broadcast

from flask import request
from flask_socketio import emit, join_room, leave_room
import json


@socketio.on('ping', namespace='/screen')
def on_ping(message):
    emit('ping', message, namespace='/screen')

@socketio.on('connect', namespace='/screen')
def on_connect():
    print('screen %s connected' % request.sid)
    emit('lobbystate', json.dumps(view.getState()), namespace='/screen')

@socketio.on('disconnect', namespace='/screen')
def on_disconnect():
    print('screen %s disconnected' % request.sid)
