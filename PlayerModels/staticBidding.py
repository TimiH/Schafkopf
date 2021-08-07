from helper import createTrumpsList
from CardValues import SUITS
from Card import Card


# Returns best TeamGame or (None,None) if no gamemode possible or sensible
def choseTeamGame(validBids, hand):
    possibleTeam = list([x for x in validBids if x[0] == 1])
    ret = (0, 0)
    if not possibleTeam:
        return (0, 0)

    # Counting U,O,T,A and
    uCount = countByRank(hand, 'U')
    oCount = countByRank(hand, 'O')
    tCount = int(len(trumpsInHandByGamemode(hand, (1,))))
    colourCount = countAllSuits(hand)  # Counts[E,G,H,S]
    total = uCount + oCount + tCount

    # Decide if possible otherwise delete list
    # 6 Trump or better
    if total >= 6:
        pass
    # 5 Trump
    elif total == 5:
        # 1 colour missing/Ace
        if any(x.rank == 'A' and x.suit != 'Herz' for x in hand) or any(colourCount[x] == 0 for x in [0, 1, 3]):
            pass
        # 2O & U
        elif oCount >= 2 and uCount <= 1:
            pass
        else:
            possibleTeam = []
    # 4 Trump containing 1 out of [OE,OG,OH], 1 U, and two Aces not heart
    elif total == 4:
        if oCount == 1 and uCount == 1 and any(x.rank == 'O' and x.suit in ['Eichel', 'Gras', 'Herz'] for x in hand):
            # two non trump aces
            acesInHand = list([x for x in hand if x.rank == 'A' and x.suit != 'Herz'])
            if len(acesInHand) >= 2:
                pass
        else:
            possibleTeam = []
    else:
        possibleTeam = []

    # Decide which of them is viable
    if possibleTeam:
        first = possibleTeam[0]
        for mode in possibleTeam:
            if colourCount[mode[1]] < colourCount[first[1]]:
                first = mode
        ret = first
    return ret


def choseSoloGame(validBids, hand):
    uCount = countByRank(hand, 'U')
    oCount = countByRank(hand, 'O')
    chosenSolo = (0, 0)
    if (uCount + oCount) < 4 or oCount < 2 or uCount < 1:
        return chosenSolo
    else:
        # Find the solo with the most trumps > 5 or leave it
        max = len(trumpsInHandByGamemode(hand, (3, 0)))
        for solo in validBids:
            if solo[0] == 3:
                trumpsInHand = trumpsInHandByGamemode(hand, solo)
                if len(trumpsInHand) >= 6 and len(trumpsInHand) > max:
                    # Check for non Trump Suits ignore A
                    cCount = countAllSuits(hand, ['O', 'U', 'A'])
                    cCount = [cCount[x] for x in range(4) if x != solo[1]]
                    if sum(cCount) <= 1:
                        chosenSolo = solo

    if chosenSolo != (0, 0):
        trumpsInHand = trumpsInHandByGamemode(hand, chosenSolo)
        if len(trumpsInHand) >= 6:
            return chosenSolo
        elif len(trumpsInHand) == 5:
            reversedSuits = dict(list(zip(list(SUITS.values()), list(SUITS.keys()))))
            # check if Colours are >=2 in order to Avoid UU6
            if countColourOfSuit(hand, reversedSuits[chosenSolo[1]]) > 2:
                chosenSolo = (0, 0)

    return chosenSolo


# Possibly look at 2U(top 2),2A
def choseWenzGame(hand):
    uCount = countByRank(hand, 'U')
    aCount = countByRank(hand, 'A')
    validBid = (0, 0)
    if uCount >= 3:
        if aCount >= 2:
            validBid = (2, 0)
        elif aCount == 1:
            ace = [x for x in hand if x.rank == 'A'][0]
            aceSuitsInHand = countAllSuits(hand)
            if aceSuitsInHand >= 3:
                validBid = (2, 0)
    return validBid

def choseWenzGameSimple(hand):
    uCount = countByRank(hand, 'U')
    aCount = countByRank(hand, 'A')
    validBid = (0, 0)
    # 4 U with A+3 or AA or AT
    if uCount == 4:
        # AAXX
        if aCount >= 2:
            validBid = (2, 0)
        elif aCount == 1:
            ace = list([x for x in hand if x.rank == 'A'])[0]
            aceSuitCount = countColourOfSuit(hand, ace.suit, ['U', 'A'])
            # A2X
            if aceSuitCount >= 2:
                validBid = (2, 0)
    elif uCount == 3:
        if aCount >= 2:
            aces = list([x for x in hand if x.rank == 'A'])
            if any(cardInHand(hand, ace.suit, 'T') for ace in aces):
                validBid = (2, 0)
        if aCount == 1:
            ace = getCardsOfRank(hand, 'A')[0]
            if cardInHand(hand, ace.suit, 'T'):
                validBid = (2, 0)
    elif uCount == 2:
        if any(cardInHand(hand, x, 'U') for x in ['Eichel', 'Gras']):
            # AAA+T|+3
            if aCount >= 2:
                aces = list([x for x in hand if x.rank == 'A'])
                colours = countAllSuits(hand, ['U', 'A'])
                if any((colours[SUITS[x.suit]]) >= 2 for x in aces):
                    validBid = (2, 0)
    return validBid

# TODO Crazy Overengineered with winrates >90%
# We are aiming for 6 Tricks and if U<4 UE is necessary
def choseWenzGameRevised(hand):
    uCount = countByRank(hand, 'U')
    aCount = countByRank(hand, 'A')
    validBid = (0, 0)
    # 4 U with A+3 or AA or AT
    if uCount == 4:
        # AAXX
        if aCount >= 2:
            validBid = (2, 0)
        elif aCount == 1:
            ace = list([x for x in hand if x.rank == 'A'])[0]
            aceSuitCount = countColourOfSuit(hand, ace.suit, ['U', 'A'])
            # ATXX
            if cardInHand(hand, ace.suit, 'T'):
                validBid = (2, 0)
            # A2X
            elif aceSuitCount >= 2:
                validBid = (2, 0)
    # 3U with UE
    elif uCount == 3:
        if cardInHand(hand, 'Eichel', 'U'):
            # UUUAAA
            if aCount >= 3:
                validBid = (2, 0)
            #UUUAAT
            if aCount == 2:
                aces = list([x for x in hand if x.rank == 'A'])
                if any(cardInHand(hand,ace.suit,'T') for ace in aces):
                    validBid = (2, 0)
            #3UATK
            if aCount == 1:
                ace = getCardsOfRank(hand,'A')[0]
                if cardInHand(hand,ace.suit,'T') and cardInHand(hand,ace.suit,'K'):
                    validBid = (2, 0)
    # 2U with UE
    elif uCount == 2:
        if cardInHand(hand, 'Eichel', 'U') and any(cardInHand(hand,x,'U') for x in ['Gras','Herz']):
            # AAAA
            if aCount == 4:
                validBid = (2, 0)
            # AAA+T|+3
            elif aCount == 3:
                aces = list([x for x in hand if x.rank == 'A'])
                colours = countAllSuits(hand, ['U', 'A'])
                if any(cardInHand(hand, x.suit, 'T') for x in aces) or any((colours[SUITS[x.suit]]) >= 3 for x in aces):
                    validBid = (2, 0)
            # AA+TT|T+2 => UUATAT
            elif aCount == 2:
                aces = list([x for x in hand if x.rank == 'A'])
                tens = [cardInHand(hand, x.suit, 'T') for x in aces]  # Checks for T of the same suit as A
                colours = countAllSuits(hand, ['U', 'A'])
                # ATAT
                if sum(tens) >= 2:
                    validBid = (2, 0)
                # ATAss e.g UUATAKO
                elif sum(tens) >= 1:
                    suitsInHand = [getCardsOfSuit(hand, s, ['U']) for s in SUITS]
                    testAT = None
                    testA2 = None
                    for suit in suitsInHand:
                        # AT
                        if rankInHand(suit, 'A') and rankInHand(suit, 'T'):
                            testAT = True
                            continue
                        # A+2
                        if rankInHand(suit, 'A') and len(suit) > 2:
                            testA2 = True
                        if testA2 and testAT:
                            validBid = (2, 0)
            # UUAT+3
            elif aCount == 1:
                aceInHand = getCardsOfRank(hand, 'A')
                if cardInHand(hand, aceInHand[0].suit, 'T'):
                    if countColourOfSuit(hand, aceInHand[0].suit,['U', 'A', 'T']) > 2:
                        validBid = (2, 0)

    return validBid


# Returns a set of Trumps in hand
def trumpsInHandByGamemode(hand, gameMode):
    trumps = createTrumpsList(gameMode)
    trumpsInHand = set(hand) & set(trumps)
    return list(trumpsInHand)


# Returns count of Rank
def countByRank(hand, rank):
    count = 0
    for card in hand:
        if card.rank == rank:
            count += 1
    return count


# Returns either a count of A,T,9,8,7 for all colours as list [E,G,H,S]
def countAllSuits(hand, ignore=None):
    if ignore is None:
        ignore = ['O', 'U']
    counts = [0, 0, 0, 0]
    for card in hand:
        if card.rank not in ignore:
            counts[SUITS[card.suit]] += 1
    return counts


# Returns count for certain suit in hand with ignore[]
def countColourOfSuit(hand, suit, ignore=None):
    if ignore is None:
        ignore = ['O', 'U', 'A']
    count = 0
    for card in hand:
        if card.suit == suit and card.rank not in ignore:
            count += 1
    return count


# BOOL:Returns True if Card in hand
def cardInHand(hand, suit, rank):
    card = Card(suit, rank)
    return card in hand


# BOOL:Returns True if any card with Rank in hand
def rankInHand(hand, rank):
    for card in hand:
        if rank == card.rank:
            return True
    return False


# Returns cards of Suit and Ignore as list in hand
def getCardsOfSuit(hand, suit, ignore=None):
    if ignore is None:
        ignore = []
    cards = list([x for x in hand if x.suit == suit and x.rank not in ignore])
    return cards


# Returns list of cards with Rank from hand
def getCardsOfRank(hand, rank):
    cards = list([x for x in hand if x.rank == rank])
    return cards


# Returns card or None
def getCardOfSuitRank(hand, suit, rank):
    card = [x for x in hand if x.suit == suit and x.rank == rank]
    if card:
        return card[0]
    else:
        return None
