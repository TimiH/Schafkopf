from CardValues import SUITS, RANKS, VALUES
from Card import Card
import random

class Deck:
    def __init__(self):
        self.cards = []
        for s in list(SUITS.keys()):
            for r in RANKS:
                self.cards.append(Card(s, r))

    def __str__(self):
        ret = ""
        for s in self.cards:
            ret += s.__str__()
            ret +=","
        return ret

    def shuffle(self,seed=None):
        if seed != None:
            random.seed(seed)
        random.shuffle(self.cards)
        # after shuffling we reset the state, as otherwise the agents run on the same state as the shuffler which
        # leasds to repeated games
        random.seed()

    def sort(self):
        self.cards.sort()

    def deal(self,number):
        ret = []
        for n in range(number):
            ret.append(self.cards.pop())
        return ret

    def dealSpecificCard(self,suit,rank):
        card = Card(suit,rank)
        self.cards.remove(card)
        return card
