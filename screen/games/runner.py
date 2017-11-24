
import time, random

interval = 0.0333
colors = ['#90EE90', '#87CEFA', '#FF4500', '#EE82EE']

def init(gameState, players):

    gameState['iteration'] = 0

    gameState['background'] = {'color': '#00BFFF'}

    gameState['ground'] = []
    gameState['ground'].append({'x': -1000, 'y': -2000, 'color': '#778899', 'width': 2000, 'height': 2000})

    lastObstacleX = 20
    gameState['obstacles'] = []
    for index in range(0, 10):
        heightY = random.randint(0, 1)
        obstaclePosX = lastObstacleX+random.randint(8, 12)
        gameState['obstacles'].append({'x': obstaclePosX, 'y': 0.2+heightY*0.8, 'color': '#778899', 'width': 0.5, 'height': 0.5})
        lastObstacleX = obstaclePosX

    gameState['players'] = []
    for index, player in enumerate(players):
        gameState['players'].append({'sid': player, 'x': index*5, 'y': 0, 'dead': False, 'color': colors[index], 'width': 0.8, 'height': 1.5})

    return gameState

def update(gameState, playerInput, lastTick):

    deltaTime = (int(round(time.time() * 1000000)) - lastTick)/1000000

    gameState['iteration'] = gameState['iteration'] + 1

    for ground in gameState['ground']:
        ground['x'] = ground['x'] - 5*deltaTime

    for obstacle in gameState['obstacles']:
        obstacle['x'] = obstacle['x'] - 5*deltaTime

    for player in gameState['players']:
        '''
        for ground in gameState['ground']:
            print(player)
            print(ground)
            print(collisionDetect(player['x'], ground['x'], player['y'], ground['y'], player['width'], ground['width'], player['height'], ground['height']))
        '''
        player['y'] = player['y'] + 9.82*deltaTime

    return gameState

def ended(gameState):
    if gameState['iteration'] == 400:
        return True
    return False

def collisionDetect(x1,x2,y1,y2,w1,w2,h1,h2):
    if x1 > x2 and x1 < x2 + w2 or x1 + w1 > x2 and x1 + w1 < x2 + w2:
        if y1 > y2 and y1 < y2 + h2 or y1 + h1 > y2 and y1 + h1 < y2 + h2:
            return True
    return False
