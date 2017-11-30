
from view import socketio, view, broadcast

from game import set_movement

from flask import request
from flask_socketio import emit, join_room, leave_room

@socketio.on('movement', namespace='/controller')
def on_movement(movement):
    set_movement(request.sid, movement)
