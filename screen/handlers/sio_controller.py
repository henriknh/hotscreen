
from view import socketio, view, broadcast

from flask import request
from flask_socketio import emit, join_room, leave_room

@socketio.on('movement', namespace='/controller')
def on_movement(message):
    print(request.sid, message)
