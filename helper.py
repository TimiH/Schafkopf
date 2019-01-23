from CardValues import SUITS,RANKS,VALUES
from Game import Game

def createTrumps(gameMode):
    trumpCards = ()
    reversed = dict(zip(SUITS.values(),SUITS.keys()))

    if gameMode ==  (2,_):
        for suit in SUITS.keys():
            trumpCards.add(Card(suit,'U'))
    if gameMode == (1,_):
        for suit in SUITS.keys():
            trumpCards.add(Card(suit,'O'))
        for suit in SUITS.keys():
            trumpCards.add(Card(suit,'U'))
        for rank in ['A','T','K','9','8','7']:
            trumpCards.add(Card('Herz',rank))

    if gameMode == (3,_):
        _,colour = gameMode
        for suit in SUITS.keys():
            trumpCards.add(Card(suit,'O'))
        for suit in SUITS.keys():
            trumpCards.add(Card(suit,'U'))
        for rank in ['A','T','K','9','8','7']:
            trumpCards.add(Card(reversed[colour],rank))
    return trumpCards
