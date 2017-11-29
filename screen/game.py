
#from view import socketio, view, broadcast

import view
import time

lobbyCountDown = 3
gameCountDown = 3

def play(gameName='runner'):

    i = 0
    while i < lobbyCountDown:
        view.broadcast('countdown', lobbyCountDown-i, '/screen')
        i+=1
        if lobbyCountDown-i >= 0:
            view.socketio.sleep(1)
    view.broadcast('countdown', -1, '/screen')

    view.view.getLobby().fillGame()
    players = view.view.getLobby().getGameQueue()

    view.view.setState("loading")

    gameState = {}

    name = "games." + gameName
    gameModule = __import__(name, fromlist=[''])

    gameState = gameModule.init(gameState, players)

    view.socketio.sleep(1)

    view.view.setState("game")

    view.broadcast('gamestate', gameState, '/screen')

    i = 0
    while i < gameCountDown:
        view.broadcast('countdown', gameCountDown-i, '/screen')
        i+=1
        if lobbyCountDown-i >= 0:
            view.socketio.sleep(1)
    view.broadcast('countdown', gameCountDown-i, '/screen')

    lastTick = int(round(time.time() * 1000000))
    i = 0
    while True:

        gameState = gameModule.update(gameState, {}, lastTick)
        lastTick = int(round(time.time() * 1000000))

        if gameModule.ended(gameState):
            break;

        view.socketio.sleep(gameModule.interval)
        #for sid in players:
        #    view.broadcast('gamestate', playerupdates, '/controller', sid)

        gameState['timestamp'] = time.time()
        view.broadcast('gamestate', gameState, '/screen')

    view.view.setState("gameover")
    view.view.getLobby().gameEnded()

    view.socketio.sleep(3)
    view.view.setState("lobby")
    view.view.setGameOver()


class Game(object):

    def __init__(self, view):
        pass
