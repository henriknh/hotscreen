from game.game import *
from lobby.lobby import *
from view.view import *

import sys, signal

game = Game()
lobby = Lobby()
view = View()

runLoop = True
while runLoop:
    try:
        print(i)
        time.sleep(0.04)
        view.emit('broadcast', {'data': i, 'time':time.time()*1000})
        i += 1
    except KeyboardInterrupt:
        runLoop = False
        view.exit()
        lobby.exit()
        game.exit()
        sys.exit()
