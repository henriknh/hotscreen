
from gevent import monkey, sleep
class Game(object):

    state = {}

    def __init__(self, view):
        self.view = view

    def exit(self):
        print('Exit Game')

    def run(self):
        while False:
            self.view.sleep(2)
            self.view.emit('gamestate', {'broadcast': 'Hej Rasmus!'})
