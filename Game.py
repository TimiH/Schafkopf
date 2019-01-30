from Card import Card
from Deck import Deck
from Bidding import Bidding
import random
from copy import deepcopy
from Player import Player
from CardValues import SUITS, RANKS, VALUES
from helper import canRunaway

class Game:
    def __init__(self, players):
        self.players = players #List of players and Positons
        self.scores = [None,None,None,None]
        self.history = ""

        self.gameMode = None
        self.bids = [(None,None)]
        self.offensivePlayers = [] #Index 0 is the WinningBid, 1 is the other player
        self.runAwayPossible = None

        self.currentTrick = None
        self.Tricks = []
        self.ranAway = False
        self.searched = False

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

    #Sets the bids, gameModes and offensivePlayers
    def setGameMode(self,bidding):
        self.bids = bidding.getBids()
        self.gameMode = bidding.winningBid
        self.offensivePlayers.append(bidding.winningIndex)

        #finds second offensive player in team mode
        reversed = dict(zip(SUITS.values(),SUITS.keys()))
        if self.gameMode[0] == 1:
            suit = self.gameMode[1]
            for p in self.players:
                for card in p.hand:
                    if card.rank == 'A':
                        if card.suit == reversed[suit]:
                            playerIndex = self.players.index(p)
                            #self.offensivePlayers.append(playerIndex)
                            self.offensivePlayers.append(playerIndex)



    def setRunAwayPossible(self):
        if len(self.offensivePlayers) >1:
            player = self.players[self.offensivePlayers[1]]
            self.runAwayPossible = canRunaway(player,self.gameMode)
        else:
            self.runAwayPossible = False

    def setSearched(self, trick):
        mode, suit = self.gameMode
        if mode != 1:
            return
        else:
            reversed = dict(zip(SUITS.values(),SUITS.keys()))
            ace =  Card(reversed[suit],'A')
            for c in trick.history:
                if c == ace:
                    self.searched = True
                    return


    def mainGame(self):
        self.setupGame()
        copy = self.copy()
        bidding = Bidding(copy)
        bidding.biddingPhase()
        print(bidding.winningIndex)
        self.setGameMode(bidding)
        self.setRunAwayPossible()
