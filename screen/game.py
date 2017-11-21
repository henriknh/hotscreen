
#from view import socketio, view, broadcast

import view

state = {}
interval = 0.0333
countDown = 5

def play():

    print('Preplay Countdown')

    i = 0
    while i <= countDown:
        view.broadcast('preplay_countdown', countDown-i, '/screen')
        i+=1
        view.socketio.sleep(1)
    view.socketio.sleep(0.5)

    view.view.getLobby().fillGame()
    players = view.view.getLobby().getGameQueue()

    view.broadcast('lobbystate', "game", '/screen')

    print('Game starts')

    i = 0
    while True:

        # Do game calculation
        if i > 200:
            print("Game over!")
            view.broadcast('lobbystate', "lobby", '/screen')
            break;
        i += 1

        view.socketio.sleep(interval)
        #for sid in players:
        #    view.broadcast('gamestate', playerupdates, '/controller', sid)
        view.broadcast('gamestate', state, '/screen')


    view.view.setState('lobby')
    view.view.getLobby().gameEnded()


class Game(object):

    def __init__(self, view):
        pass
