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

#TODO testing requirements
def recreateHandsfromHistory(history):
    hands = [[],[],[],[]]

    for trick in history:
        lead = trick[1]
        winner = trick[2]
        for card in trick[0]:
            hands[lead].append(card)
            lead = (lead+1)%4
    return hands

#allows using sort using Suit
def bySuit(card):
    return card.suit

#allows using sort Rank
def byRank(card):
    return card.rank

#Sorts hand using OUsuit
def sortHand(hand):
    #filter for O and U
    oSorted = filter(lambda x: x.rank == 'O', hand)
    uSorted = filter(lambda x: x.rank == 'U', hand)
    otherCards = filter(lambda x: x.rank != 'U' and x.rank != 'O', hand)

    #ugly if statements in case list empty
    sortedHand = []
    if oSorted:
        oSorted = sorted(oSorted,key=bySuit)
        [sortedHand.append(x) for x in oSorted]
    if uSorted:
        uSorted = sorted(uSorted,key=bySuit)
        [sortedHand.append(x) for x in uSorted]
    if otherCards:
        otherCards = sorted(otherCards, key=bySuit)
        [sortedHand.append(x) for x in otherCards]

    return sortedHand
