import pickle
import requests
import socket
# need pillow installed for image rendering for QR

class Registration(object):

    def __init__(self):
        self.hash = ''
        self.code = ''
        self.qr = ''

    def register(self, ip, port):
        url = 'http://localhost:5000/register/%s/%d' % (ip, port)
        r = requests.post(url)
        status_code = r.status_code
        if status_code != 200:
            print('Something went wrong, got ' + status_code, file=sys.stderr)
            return -1
        else:
            response = pickle.loads(r.content) # unbox the response content
            self.hash = response['hash'] # not really needed
            self.code = response['code'] # should be displayed
            self.qr = response['qr']
            return

    def saveQR(self):
        img = self.qr.make_image()
        img.save('static/media/qr.png') # can also use .jpeg, .bmp

reg = Registration()
ip = socket.gethostbyname(socket.gethostname())
port = 5000
reg.register(ip, port)
reg.saveQR()

from view import *
