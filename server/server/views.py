from server import app
from flask import request

import pyqrcode
import pickle
import hashlib
import random
import string

from server.classes.multikey_dict import *

deviceDict = MultiKeyDictionary() # need db to save it

@app.route('/')
def index():
    return 'Index page'

@app.route('/devices')
def getDevices():
    return deviceDict.str()

@app.route('/play/<string:ID>', methods=['GET'])
def startplaying(ID):
    try:
        address = deviceDict[ID] # return parameter, might no be in dictionary
    except KeyError:
        return "Couldn't find device"
    return ID # return template with parameters, go back one step

@app.route('/register/<string:ip>/<int:port>', methods=['POST'])
# POST since will add new information to the server, update list of devices
def register(ip, port):
    if request.method == 'POST': # will automatic show 405 error
        address = (ip, port) #should info add to list
        hashID = getHashID(address) # get an ID which depends on the address
        codeID = getCodeID()
        addDevice(hashID, address) # add hash
        addDevice(codeID, address) #add digit code
        qr = createQR(hashID)
        #pickled_qr = pickle.dumps(qr)
        msg = { 'qr': qr, 'code': codeID, 'hash': hashID }
        response = pickle.dumps(msg)
        return response

def createQR(deviceID):
    url = 'http://130.240.5.87/play/' + deviceID
    qr = pyqrcode.create(url) # qr is a Object of type bytes
    return qr

def getCodeID(): # should check so not already in dictionary
    s = ""
    s = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    try:
        deviceDict[s]
        getCode()
    except KeyError:
        return s # doesn't already

def getHashID(address):
    string = '%s:%d' % address
    hash_obj = hashlib.sha1(string.encode())
    hex_dig = hash_obj.hexdigest()
    return hex_dig

def addDevice(deviceID, address):
    deviceDict[deviceID] = address
    return
