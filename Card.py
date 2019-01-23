import random
import itertools
import operator
from CardValues import SUITS, RANKS, VALUES

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = VALUES[rank]

    def __str__(self):
        return "{}{}".format(self.rank,self.suit[0])

    def __lt__(self,other):
        return (self.suit,self.rank,) < (other.suit,other.rank)

    def __eq__(self, other):
        if self.suit == other.suit and self.rank == other.rank:
            return True
        else:
             return False

    def __repr__(self):
        return "{}{}".format(self.rank,self.suit[0])
