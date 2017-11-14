from server import app
from flask import request, render_template, url_for

import pyqrcode
import pickle
import hashlib
import random
import string

from server.classes.multikey_dict import *
from server import MAX_KEYS # max keys for one device
from server import deviceDict # import the dictionary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices')
def getDevices():
    return deviceDict.str()

@app.route('/play/<string:ID>', methods=['GET'])
def startplaying(ID):
    try:
        address = deviceDict[ID] # return parameter, might no be in dictionary
    except KeyError:
        return "Couldn't find device"
    ip, port = address
    return render_template('play.html', ip=ip, port=port)

@app.route('/register/<string:ip>/<int:port>', methods=['POST'])
# POST since will add new information to the server, update list of devices
def register(ip, port):
    if request.method == 'POST': # will automatic show 405 error
        address = (ip, port) #should info add to list
        hashID = getHashID(address) # get an ID which depends on the address
        codeID = getCodeID()
        addDevice(hashID, address) # add the hash id
        addDevice(codeID, address) #add digit code
        qr = createQR(hashID)
        msg = { 'qr': qr, 'code': codeID, 'hash': hashID }
        response = pickle.dumps(msg)
        saveDictionary()
        return response

def createQR(deviceID):
    url = 'http://130.240.5.87/play/' + deviceID
    qr = pyqrcode.create(url) # qr is a Object of type bytes
    return qr

def getCodeID():
    s = ""
    s = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if deviceDict.has(s): # key already exist
        i = 0
        while i < 5: # try 5 time for new code
            s = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if deviceDict.has(s): # again, code exists
                i += 1
            else:
                return s
        return "Couldn't find a new code"
    return s

def getHashID(address):
    string = '%s:%d' % address
    hash_obj = hashlib.sha1(string.encode())
    hex_dig = hash_obj.hexdigest()
    return hex_dig

def addDevice(deviceID, address): # first, need to check so not an update
    try:
        if len(deviceDict.values[address]) < MAX_KEYS: # ok to add
            deviceDict[deviceID] = address
            return
        else: # update already existing keys instead of adding new one
            keys = deviceDict.values[address]
            for key in keys:
                deviceDict[key] = address
    except KeyError:
        deviceDict[deviceID] = address
    return

def saveDictionary():
    with open('deviceDictionary.pickle', 'wb') as handle:
        pickle.dump(deviceDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
