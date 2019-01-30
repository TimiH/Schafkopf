from CardValues import SUITS,RANKS,VALUES
from Card import Card
# from Game import Game
from copy import copy

def createTrumps(gameMode):
    trumpCards = set()
    reversed = dict(zip(SUITS.values(),SUITS.keys()))
    mode = gameMode[0]
    if mode ==  2:
        for suit in ['Eichel','Gras','Herz','Schellen']:
            trumpCards.add(Card(suit,'U'))
    elif mode == 1:
        for suit in ['Eichel','Gras','Herz','Schellen']:
            trumpCards.add(Card(suit,'O'))
        for suit in ['Eichel','Gras','Herz','Schellen']:
            trumpCards.add(Card(suit,'U'))
        for rank in ['A','T','K','9','8','7']:
            trumpCards.add(Card('Herz',rank))
    elif mode == 3:
        _,colour = gameMode
        for suit in ['Eichel','Gras','Herz','Schellen']:
            trumpCards.add(Card(suit,'O'))
        for suit in SUITS.keys():
            trumpCards.add(Card(suit,'U'))
        for rank in ['A','T','K','9','8','7']:
            trumpCards.add(Card(reversed[colour],rank))
    return trumpCards

def createTrumpsList(gameMode):
    trumpCards = []
    reversed = dict(zip(SUITS.values(),SUITS.keys()))
    mode = gameMode[0]
    if mode ==  2:
        for suit in ['Eichel','Gras','Herz','Schellen']:
            trumpCards.append(Card(suit,'U'))
    elif mode == 1:
        for suit in ['Eichel','Gras','Herz','Schellen']:
            trumpCards.append(Card(suit,'O'))
        for suit in ['Eichel','Gras','Herz','Schellen']:
            trumpCards.append(Card(suit,'U'))
        for rank in ['A','T','K','9','8','7']:
            trumpCards.append(Card('Herz',rank))
    elif mode == 3:
        _,colour = gameMode
        for suit in ['Eichel','Gras','Herz','Schellen']:
            trumpCards.append(Card(suit,'O'))
        for suit in ['Eichel','Gras','Herz','Schellen']:
            trumpCards.append(Card(suit,'U'))
        for rank in ['A','T','K','9','8','7']:
            trumpCards.append(Card(reversed[colour],rank))
    return trumpCards

#Assumes that player passed has the ace
def canRunaway(player,gameMode):
    hand = set(copy(player.hand))
    trumps = createTrumps(gameMode)
    #Only leave colours
    hand -= trumps
    reversed = dict(zip(SUITS.values(),SUITS.keys()))
    suit = reversed[gameMode[1]]
    hand = list(filter(lambda x: x.suit == suit,hand))
    if len(hand) >= 4:
        return True
    else:
        return False
