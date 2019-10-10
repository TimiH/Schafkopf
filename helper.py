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
    return Card.suit

#allows using sort Rank
def byRank(card):
    return Card.rank

#Sorts hand using OUsuit
def sortHand(hand):
    print(hand)
    sortedHand = []
    #filter for O and U
    oSorted = filter(lambda x: x.rank == 'O', hand)
    uSorted = filter(lambda x: x.rank == 'U', hand)
    otherCards = filter(lambda x: x.rank != 'U' and x.rank != 'O', hand)
    print("unsorted: ",oSorted, uSorted, otherCards)
    if oSorted:
        oSorted = sorted(oSorted,key=bySuit)
        [sortedHand.append(x) for x in oSorted]
    if uSorted:
        uSorted = sorted(uSorted,key=bySuit)
        [sortedHand.append(x) for x in uSorted]
    if otherCards:
        otherCards = sorted(otherCards, key=bySuit)

    print("sorted: ",oSorted, uSorted)
    #otherCards = [x for x in hand if not oSorted]
    # if oSorted:
    #     sortedHand + oSorted
    # if uSorted:
    #     sortedHand + uSorted
    # #sortedHand.append(otherCards.sort(key=bySuit))
    print(sortedHand)
    #find
    return sortHand

#Sorts hands for gamemode and returns hand to player
#def sortHand(hand,gameMode):
    #check for gameMode
    #if None (0,0) sort hands standard
    #if Team (1,) sort O U Hearts,Eichel,Gras, Schellen
    #if Solo (4,) sort O U Color
    #if Wenz (2,) sort U Color
    #return hand
