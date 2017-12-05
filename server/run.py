#!/usr/bin/python3.5

from server import app
from OpenSSL import SSL

def start():
	try:
		context = ('hotscreen.crt', 'hotscreen.key')
		app.run(host='0.0.0.0', port=5000, debug = False)
	except Exception:
		print('Could not start server')
		raise

if __name__ == '__main__':
	start()
