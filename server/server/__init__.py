from flask import Flask
app = Flask(__name__)

from server.classes.multikey_dict import *

import pickle

MAX_KEYS = 2

def loadDictionary():
    with open('deviceDictionary.pickle', 'rb') as handle:
        return pickle.load(handle)

deviceDict = loadDictionary()

from server import views
