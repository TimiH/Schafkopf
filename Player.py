from GameModes import MODES
from CardValues import SUITS,RANKS
from Card import Card
import random

class Player:
    def __init__(self,name):
        self.name = name
        self.hand = []
    ##TODO __repr__ and __str__

    def setHand(self,cards):
        self.hand = cards

    def makeBid(self,validBids):
        return random.choice(validBids)

    def playCard(self,state):
        pass

    def sortHand(self,state):
        pass
