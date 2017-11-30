
import time, random

interval = 1/30
colors = ['#EE82EE', '#90EE90', '#87CEFA', '#FF4500']

def init(gameState, players):

    gameState['iteration'] = 0

    gameState['background'] = {'color': '#101010'}

    return gameState

def update(gameState, players_movement, lastTick):

    deltaTime = (int(round(time.time() * 1000000)) - lastTick)/1000000

    gameState['iteration'] = gameState['iteration'] + 1

    return gameState

def ended(gameState):
    ended = True


    return ended

def getPlayerState(gameState, sid):
    for player in gameState['players']:
        if player['sid'] == sid:
            return {'backgroundcolor': player['color'], 'space': {'score': player['score']}}
    return {}

quiz = [
    {'question': 'qwe'}
]
