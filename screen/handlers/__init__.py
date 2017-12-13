from flask import Blueprint

handlers = Blueprint('handlers', __name__)

from . import routes, sio_lobby, sio_controller, sio_screen
