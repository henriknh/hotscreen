
import time, random

#interval = 1/30
interval = 1/30
colors = ['#EE82EE', '#90EE90', '#87CEFA', '#FF4500']


def init(gameState, players):

    gameState['iteration'] = 0

    gameState['background'] = {'color': '#101010'}

    gameState['asteroids'] = []
    for index in range(0, 15):
        gameState['asteroids'].append(newAsteroid())

    player_placement_interval = 100/(len(players)+1)
    gameState['players'] = []
    for index, player in enumerate(players):
        gameState['players'].append({'sid': player, 'x': (index+1)*player_placement_interval, 'y': 80, 'dead': False, 'color': colors[index], 'width': 6, 'height': 10, 'score': 0})

    return gameState

def update(gameState, players_movement, lastTick):

    deltaTime = (int(round(time.time() * 1000000)) - lastTick)/1000000

    gameState['iteration'] = gameState['iteration'] + 1

    for player in gameState['players']:
        if player['dead'] == False:
            player['score'] = player['score'] + 1
            for player_movement in players_movement:
                if player_movement['sid'] == player['sid']:
                    player['x'] = player['x'] + int(player_movement['movement']["beta"])*deltaTime
                    if player['x'] <= 5:
                        player['x'] = 5
                    if player['x'] >= 95:
                        player['x'] = 95

    for asteroid in gameState['asteroids']:
        if asteroid['dead']:
            continue

        asteroid['y'] = asteroid['y'] + asteroid['deltaY']*deltaTime

        if asteroid['y'] > 100:
            asteroid['dead'] = True
            gameState['asteroids'].append(newAsteroid())

        for player in gameState['players']:
            if collide(player, asteroid):
                player['dead'] = True

    return gameState

def ended(gameState):
    ended = True
    for player in gameState['players']:
        if not player['dead']:
            ended = False
    return ended

def getPlayerState(gameState, sid):
    for player in gameState['players']:
        if player['sid'] == sid:
            return {'score': player['score']}
    return {}

def newAsteroid():
    w = random.randint(4, 8)
    h = random.randint(4, 8)
    if random.uniform(0, 1) < 0.1:
        w = w*3
        h = h*3
    return {'x': random.uniform(0, 100), 'y': -20-random.uniform(0, 100), 'dead': False, 'color': '#778899', 'width': w, 'height': h, 'deltaY': 25/w*h}

def collide(obj1, obj2):
    if (obj1['x']+obj1['width']<obj2['x'] or obj2['x']+obj2['width']<obj1['x'] or obj1['y']+obj1['height']<obj2['y'] or obj2['y']+obj2['height']<obj1['y']):
        return False
    else:
        return True
