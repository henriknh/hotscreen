
#from view import socketio, view, broadcast

import view
import time

lobbyCountDown = 3
minLoadingTime = 8
gameCountDown = 3

ticks = 0

players_movement = []

def play(gameName):

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
    ticks = 0

    timeStartLoading = time.time()

    name = "games." + gameName
    gameModule = __import__(name, fromlist=[''])

    loadingTime = time.time() - timeStartLoading


    view.broadcast('loadingtips', {'message': gameModule.instruction}, '/screen')

    gameState = gameModule.init(gameState, players)

    if loadingTime < minLoadingTime:
        view.socketio.sleep(minLoadingTime-loadingTime)

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

        gameState = gameModule.update(gameState, players_movement, lastTick)
        lastTick = int(round(time.time() * 1000000))

        if gameModule.ended(gameState):
            break;

        view.socketio.sleep(gameModule.interval)
        for sid in players:
            view.broadcast('playerstate', gameModule.getPlayerState(gameState, sid), '/controller', sid)

        gameState['timestamp'] = time.time()
        view.broadcast('gamestate', gameState, '/screen')

        ticks = ticks + 1

    view.view.setState("gameover")
    view.socketio.sleep(3)

    view.view.setState("lobby")
    view.view.setGameOver()

def set_movement(sid, movement):
    updated = False
    for player_movement in players_movement:
        if player_movement['sid'] == sid:
            player_movement['movement'] = movement
            updated = True
    if not updated:
        players_movement.append({'sid': sid, 'movement': movement})


class Game(object):

    def __init__(self, view):
        pass
