from flask import Flask
app = Flask(__name__)

from server.classes.multikey_dict import *
from threading import Lock

import pickle

MAX_KEYS = 2
lock = Lock()

def loadDictionary():
    try:
        with open('deviceDictionary.pickle', 'rb') as handle:
            return pickle.load(handle)
    except FileNotFoundError:
        return MultiKeyDictionary()

deviceDict = loadDictionary()

from server import views
