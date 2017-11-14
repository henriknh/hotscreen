from flask import Flask, request
app = Flask(__name__)

import pyqrcode
import pickle
import hashlib
import random
import string

import server.classes.multikey_dict

import server.views

deviceDict = MultiKeyDictionary() # need db to save it
