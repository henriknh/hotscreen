from server import app
from flask import request, render_template, url_for, redirect

import pickle
import hashlib
import random
import string
import qrcode
import time
import atexit
import requests

from server.classes.multikey_dict import *
from server import MAX_KEYS # max keys for one device
from server import deviceDict # import the dictionary
from server import lock

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

def pingDevices():
    print('Checking devices')
    value_list = deviceDict.values.keys()
    for val in list(value_list):
        url = 'http://%s:%d/heartbeat' % val
        try:
            r = requests.get(url, timeout=5)
            if r.status_code != 200:
                removeDevice(val)
        except (requests.exceptions.RequestException, requests.exceptions.Timeout):
            removeDevice(val)
        saveDictionary()

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=pingDevices,
    trigger=IntervalTrigger(seconds=15), # may only be needed once a day perhaps
    id='heartbeat_job',
    name='Check if devices in dictionary are still alive.',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices')
def getDevices():
    if deviceDict.str() == "":
        return "No devices are registered..."
    return deviceDict.str()

@app.route('/play', methods=['POST']) # at index page, code input
def play():
    code = request.form['code']
    return redirect(url_for('startplaying', ID=code))

@app.route('/play/dummy', methods=['GET'])
def dummyroute():
    return render_template('play.html', ip='localhost', port=5050)

@app.route('/play/<string:ID>', methods=['GET'])
def startplaying(ID):
    ID = ID.upper()
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
        hashID = getHashID(address).upper() # get an ID which depends on the address
        codeID = getCodeID()
        newDevice(hashID, address) # add the hash id
        newDevice(codeID, address) #add digit code
        qr = createQR(hashID)
        msg = { 'qr': qr, 'code': codeID, 'hash': hashID }
        response = pickle.dumps(msg)
        saveDictionary()
        return response

def createQR(deviceID):
    url = 'https://130.240.5.87:5000/play/' + deviceID
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr

def getCodeID():
    s = ""
    size = 5
    s = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
    if deviceDict.has(s): # key already exist
        i = 0
        while i < 5: # try 5 time for new code
            s = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
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

def newDevice(deviceID, address): # first, need to check so not an update
    try:
        if len(deviceDict.values[address]) < MAX_KEYS: # ok to add
            addDevice(deviceID, address)
            return
        else: # update already existing keys instead of adding new one
            keys = deviceDict.values[address]
            for key in keys:
                addDevice(key, address)
    except KeyError:
        addDevice(deviceID, address)
    return

def addDevice(key, value):
    lock.acquire()
    deviceDict[key] = value
    lock.release()

def removeDevice(value):
    lock.acquire()
    deviceDict.remove(value)
    lock.release()

def saveDictionary():
    lock.acquire()
    with open('deviceDictionary.pickle', 'wb') as handle:
        pickle.dump(deviceDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    lock.release()
