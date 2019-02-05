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
        for bid in validBids:
            if bid[0] == 1:
                return bid
        return (None,None)
        #return random.choice(validBids)

    def playCard(self,validCards,state):
        print("{} Hand:{}".format(self.name,self.hand))
        print("{} Valid:{}".format(self.name,validCards))
        card = random.choice(validCards)
        print("{} ->:{}".format(self.name,card))
        return card

    def sortHand(self,state):
        pass
