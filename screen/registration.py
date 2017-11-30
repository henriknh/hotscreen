import pickle
import requests
import socket, os

class Registration(object):

    def __init__(self):
        self.hash = ''
        self.code = ''
        self.qr = ''

    def register(self, port):

        ipaddr = ""
        try:
            gw = os.popen("ip -4 route show default").read().split()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((gw[2], 0))
            ipaddr = s.getsockname()[0]
        except IndexError:
            ipaddr = socket.gethostbyname(socket.gethostname())

        url = 'http://http://130.240.5.87:5000/register/%s/%d' % (ipaddr, port)
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

            self.saveQR()
            return

    def saveQR(self):
        img = self.qr.make_image()
        img.save('static/media/qr.png') # can also use .jpeg, .bmp
