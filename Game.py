from Card import Card
from Deck import Deck
from Bidding import Bidding
import random
from copy import deepcopy
from Player import Player

class Game:
    def __init__(self, players):
        self.players = players #List of players and Positons
        self.scores = [None,None,None,None]
        self.history = ""
        self.gameMode = None
        self.currentTrickNumber = None
        self.leadingPlayer = 0
        self.ranAway = False
        self.searched = False
        self.bids = [(None,None)]
        self.rewards = [0,0,0,0]
        self.trumpCards = ()

    def playGame(self):
        pass

    def playTrick(self):
        pass

    def setupGame(self):
        deck = Deck()
        deck.shuffle()

        #Dealing cards
        for p in self.players:
            p.setHand(deck.deal(8))

    def shufflePositon(self):
        random.shuffle(self.players)

    def copy(self):
        return deepcopy(self)

    def getPlayerForTurn():
        pass

    def setHistory(self):
        pass

    def mainGame(self):
        self.setupGame()
        bidding = Bidding(self.copy)
        bidding.biddingPhase()
        self.bids = bidding.bids
