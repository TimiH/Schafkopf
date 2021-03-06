from GameModes import MODES
from CardValues import SUITS,RANKS
from Card import Card
import random

class Player(object):
    def __init__(self,name):
        self.name = name
        self.hand = []

    ##TODO __repr__ and __str__

    def setHand(self,cards):
        self.hand = cards

    def makeBid(self,validBids):
        # for bid in validBids:
        #     if bid[0] == 1:
        #         return bid
        # return (None,None)
        card = random.choice(validBids)
        return card

    def playCard(self,validCards,state,trickHistory):
        if not validCards:
            print(self.name, "STOP NO VALID CARDS with Hand:",self.hand)
        card = random.choice(validCards)
        # if "SampleMaster" in self.name:
        #     print("{} ,Hand:{},History: {},Playing: {},validCards: {}".format(self.name,self.hand,trickHistory,card,validCards))
        return card

    def sortHand(self,state):
        pass

    def getPosition(self,gamestate):
        for n in range(4):
            if gamestate.players[n].name == self.name:
                return n
