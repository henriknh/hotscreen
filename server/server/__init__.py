from flask import Flask
app = Flask(__name__)

from server.classes.multikey_dict import *

MAX_KEYS = 2
deviceDict = MultiKeyDictionary()

from server import views
