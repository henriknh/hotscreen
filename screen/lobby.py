from queues import *

class Lobby(object):

    minPlayers = 1
    maxPlayers = 4

    def __init__(self, view):
        self.view = view

        self.lobby = Queue()
        self.game = Queue()

    def exit(self):
        print('Exit Lobby')

    '''
        Lobby Players
    '''

    def connectToLobby(self, name):
        if self.lobby.exists(name):
            return False
        self.lobby.append(name)
        self.view.checkEnoughPlayers()
        self.view.broadcast('queue_updated', self.getLobbyQueue(), '/screen')
        return True

    def disconnectFromLobby(self, name):
        return self.lobby.remove(name)
        self.view.broadcast('queue_updated', self.getLobbyQueue(), '/screen')

    def getLobbySize(self):
        return self.lobby.size()

    def getLobbyQueue(self):
        return self.lobby.getQueue()

    '''
        Game Players
    '''

    def isEnough(self):
        if self.getLobbySize() >= self.minPlayers:
            return True
        return False

    def fillGame(self):
        if not self.isEnough():
            return False

        nrOfPlayers = self.getLobbySize()

        if(nrOfPlayers > self.maxPlayers):
            nrOfPlayers = self.maxPlayers

        for i in range(0, nrOfPlayers):
            player = self.lobby.pop()
            self.game.append(player)
        self.view.broadcast('queue_updated', self.getLobbyQueue(), '/screen')
        return True

    def gameEnded(self):
        for i in range(0, self.game.size()):
            self.game.pop()
        self.view.checkEnoughPlayers()
        self.view.broadcast('queue_updated', self.getLobbyQueue(), '/screen')
        return True

    def getGameQueue(self):
        return self.game.getQueue()
