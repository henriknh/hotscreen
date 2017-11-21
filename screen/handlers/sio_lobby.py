
from view import socketio, view, broadcast
from game import play

from flask import request
from flask_socketio import emit, join_room, leave_room

@socketio.on('connect', namespace='/controller')
def on_connect():
    print('%s connected' % request.sid)
    view.getLobby().connectToLobby(request.sid)

@socketio.on('disconnect', namespace='/controller')
def on_disconnect():
    print('%s disconnected' % request.sid)
    view.getLobby().disconnectFromLobby(request.sid)

@socketio.on('ping', namespace='/controller')
def on_ping(message):
    emit('ping', message, namespace='/controller')
