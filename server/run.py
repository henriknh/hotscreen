#!/usr/bin/env python

from server import app

def start():
	try:
		app.run(host='0.0.0.0')
	except Exception:
		print('Could not start server')
		raise

if __name__ == '__main__':
	start()
