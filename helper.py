from CardValues import SUITS, RANKS, VALUES, COMPARERANKS
from Card import Card
# from Game import Game
from copy import copy

def createTrumps(gameMode):
    trumpCards = set()
    reversed = dict(list(zip(list(SUITS.values()), list(SUITS.keys()))))
    mode = gameMode[0]
    if mode == 2:
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
        _, colour = gameMode
        for suit in ['Eichel', 'Gras', 'Herz', 'Schellen']:
            trumpCards.add(Card(suit, 'O'))
        for suit in list(SUITS.keys()):
            trumpCards.add(Card(suit, 'U'))
        for rank in ['A', 'T', 'K', '9', '8', '7']:
            trumpCards.add(Card(reversed[colour], rank))
    return trumpCards

def createTrumpsList(gameMode):
    trumpCards = []
    reversed = dict(list(zip(list(SUITS.values()), list(SUITS.keys()))))
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
    reversed = dict(list(zip(list(SUITS.values()), list(SUITS.keys()))))
    suit = reversed[gameMode[1]]
    hand = list([x for x in hand if x.suit == suit])
    if len(hand) >= 4:
        return True
    else:
        return False

#TODO testing requirements
def recreateHandsfromHistory(history):
    hands = [[], [], [], []]

    for trick in history:
        lead = trick[1]
        winner = trick[2]
        for card in trick[0]:
            hands[lead].append(card)
            lead = (lead + 1) % 4
    return hands


# allows using sort using Suit
def bySuit(card):
    return card.suit


# allows using sort Rank
def byRank(card):
    rank = card.rank
    cmp = COMPARERANKS[rank]
    return cmp


# TODO SORT by trump as Herz is at the end
# Sorts hand using OUsuit
def sortHand(hand):
    # filter for O and U
    oSorted = [x for x in hand if x.rank == 'O']
    uSorted = [x for x in hand if x.rank == 'U']
    otherCards = [x for x in hand if x.rank != 'U' and x.rank != 'O']

    # ugly if statements in case list empty
    sortedHand = []
    if oSorted:
        oSorted = sorted(oSorted, key=bySuit)
        [sortedHand.append(x) for x in oSorted]
    if uSorted:
        uSorted = sorted(uSorted, key=bySuit)
        [sortedHand.append(x) for x in uSorted]
    if otherCards:
        otherCards = sorted(otherCards, key=bySuit)
        [sortedHand.append(x) for x in otherCards]

    return sortedHand


def sortHandByGameMode(hand, gameMode):
    if gameMode[0] == 2:
        return sortHandWenz(hand)
    oSorted = [x for x in hand if x.rank == 'O']
    oSorted = sorted(oSorted,key=bySuit)
    uSorted = [x for x in hand if x.rank == 'U']
    uSorted = sorted(uSorted,key=bySuit)

    eSorted = [x for x in hand if x.suit == 'Eichel' and x.rank != 'U' and x.rank != 'O']
    gSorted = [x for x in hand if x.suit == 'Gras' and x.rank != 'U' and x.rank != 'O']
    hSorted = [x for x in hand if x.suit == 'Herz' and x.rank != 'U' and x.rank != 'O']
    sSorted = [x for x in hand if x.suit == 'Schellen' and x.rank != 'U' and x.rank != 'O']
    colors = {}
    if eSorted:
        eSorted = sorted(eSorted, key=byRank)
        colors[0] = eSorted
    if gSorted:
        gSorted = sorted(gSorted, key=byRank)
        colors[1] = gSorted
    if hSorted:
        hSorted = sorted(hSorted, key=byRank)
        colors[2] = hSorted
    if sSorted:
        sSorted = sorted(sSorted, key=byRank)
        colors[3] = sSorted
    sortedHand = [] + oSorted + uSorted
    if gameMode[0] == 1:
        sortedHand = [] + oSorted + uSorted + hSorted
        for i in [0, 1, 3]:
            if i in colors:
                sortedHand += colors[i]
    if gameMode[0] == 3:
        order = [0, 1, 2, 3]
        order.remove(gameMode[1])
        sortedHand += colors[gameMode[1]]
        for i in order:
            sortedHand += colors[i]
    return sortedHand


def sortHandWenz(hand):
    # filter U and colours
    uSorted = [x for x in hand if x.rank == 'U']
    eSorted = [x for x in hand if x.suit == 'Eichel' and x.rank != 'U']
    gSorted = [x for x in hand if x.suit == 'Gras' and x.rank != 'U']
    hSorted = [x for x in hand if x.suit == 'Herz' and x.rank != 'U']
    sSorted = [x for x in hand if x.suit == 'Schellen' and x.rank != 'U']

    sortedHand = []
    if uSorted:
        uSorted = sorted(uSorted, key=bySuit)
        sortedHand += uSorted
    if eSorted:
        eSorted = sorted(eSorted, key=byRank)
        sortedHand += eSorted[::-1]
    if gSorted:
        gSorted = sorted(gSorted, key=byRank)
        sortedHand += gSorted[::-1]
    if hSorted:
        hSorted = sorted(hSorted,key=byRank)
        sortedHand += hSorted[::-1]
    if sSorted:
        sSorted = sorted(sSorted,key=byRank)
        sortedHand += sSorted[::-1]
    return sortedHand

#modified mod function for ringTest
def modRing(a, b):
    return (((a % b) + b) % b)


# Checks if for position if player has already played a card in currentTrick. used it SampleMaster
def ringTest(lead, cardsPlayed, testPos):
    end = (lead + cardsPlayed) % 4
    a = modRing((testPos - lead), 4)
    b = modRing((end - lead), 4)
    return a < b


# gets trick history and and gameMode and determines the winner
def getTrickWinnerIndex(trickHistory, gameMode):
    trumps = createTrumpsList(gameMode)
    # trumpsPlayed = [card for card in trickHistory if card in trumps] #TODO use sets here
    trumpsPlayed = list(set(trickHistory) & set(trumps))
    if trumpsPlayed:
        winningTrumpIndex = min([trumps.index(card) for card in trumpsPlayed])
        winningCard = trumps[winningTrumpIndex]
        winningCardIndex = trickHistory.index(winningCard)
        return winningCardIndex
    else:
        firstSuit = trickHistory[0].suit
        winningRankIndex = min([RANKS.index(card.rank) for card in trickHistory if card.suit == firstSuit])
        winningCardIndex = trickHistory.index(Card(firstSuit, RANKS[winningRankIndex]))
        return winningCardIndex


def sumTrickHistory(trickHistory):
    score = 0
    for card in trickHistory:
        score += card.value
    return score
