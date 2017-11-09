class Lobby(object):
    def __init__(self, view):

        self.lobbyQueue = []
        self.gameQueue = []
        ## Ready? player ready?
        self.gameEnoughPlayers = False

    def exit(self):
        print('Exit Lobby')


    ## korta ner lite??? ..
    def addPlayerLobby(self, name):
        self.lobbyQueue.append(name)
    def getFirstPlayerLobby(self):
        if len(self.lobbyQueue) > 0:
            return self.lobbyQueue[0]
        return "-1"
    def getLobbyQueue(self):
        return self.lobbyQueue
    def removeFirstPlayerLobby(self):
        self.lobbyQueue.pop(0)

    def addPlayerGame(self, name):
        self.gameQueue.append(name)
    def getFirstPlayerGame(self):
        if len(self.gameQueue) > 0:
            return self.gameQueue[0]
        return "Lobby is empty"
    def getGameQueue(self):
        return self.gameQueue
    def removeFirstPlayerGame(self):
        self.gameQueue.pop(0)


##  Spelare ansluter till lobby
    def connectToLobby(self, name):
        for p in self.lobbyQueue:
            if p == name:
                return "Player is already in queue"
        self.addPlayerLobby(name)
        return "player added to queue"

    def disconnectFromLobby(self, name):
        self.lobbyQueue.remove(name)
        return "player: " + name + " was removed from queue"

##  Anslut spelare till game (1a från lobby till game)
##  Kolla antal platser?
    def connectToGame(self):
        tmp = self.getFirstPlayerLobby() ## Behövs inte egentligen
        self.removeFirstPlayerLobby()
        self.addPlayerGame(tmp)
        return "player: " + tmp + " was added to the game queue"

    def disconnectFromGame(self, name):
        self.lobbyQueue.remove(name)
        return "player: " + name + " was removed from queue"

    ## Kolla antal spelare, lägg till fler?
    def fillGame(self, playersMin, playersMax):
        for i in range(playersMin - len(self.getGameQueue())):
            if len(self.getLobbyQueue()) > 0:
                self.connectToGame()
        for i in range(playersMax - len(self.getGameQueue())):
            if len(self.getLobbyQueue()) > 0:
                self.connectToGame()

    ## Clear the game queue (Kallas när spelet är slut?)
    def clearGameQueue():
        self.gameQueue.clear()
