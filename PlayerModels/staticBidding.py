from helper import createTrumps
from CardValues import RANKS, SUITS
from Card import Card


# Returns best TeamGame or (None,None) if no gamemode possible or sensible
def choseTeamGame(validBids, hand):
    possibleTeam = list(filter(lambda x: x[0] == 1, validBids))
    ret = (None, None)
    if not possibleTeam:
        return (None, None)

    # Counting U,O,T,A and
    uCount = countByRank(hand, 'U')
    oCount = countByRank(hand, 'O')
    tCount = int(len(trumpsInHandByGamemode(hand, (1,))))
    aCount = countByRank(hand, 'A')
    colourCount = countAllSuits(hand)  # Counts[E,G,H,S]
    total = uCount + oCount + tCount
    print('Total: ' + str(total), 'Ober: ' + str(oCount), ' Unter:' + str(uCount), ' #Asse:' + str(aCount))

    # Decide if possible otherwise delete list
    # 6 Trump or better
    if total >= 6:
        print('Option 6 Trump')
        pass
    # 5 Trump
    elif total == 5:
        # 1 colour missing/Ace
        if any(x.rank == 'A' and x.suit != 'Herz' for x in hand) or any(colourCount[x] == 0 for x in [0, 1, 3]):
            print('Option 5 Trump: Fehl or Ace')
            pass
        # 2O & U
        elif oCount >= 2 and uCount <= 1:
            print('Option 5 Trump: 2O&1U')
            pass
    # 4 Trump containing 1 out of [OE,OG,OH], 1 U, and two Aces not heart
    elif total == 4:
        if oCount == 1 and uCount == 1 and any(x.rank == 'O' and x.suit in ['Eichel', 'Gras', 'Herz'] for x in hand):
            # two non trump aces
            acesInHand = list(filter(lambda x: x.rank == 'A' and x.suit != 'Herz', hand))
            if len(acesInHand) >= 2:
                print('Option 4 Trump')
                pass
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
    chosenSolo = (None, None)
    if (uCount + oCount) < 3:
        return chosenSolo
    else:
        # Find the solo with the most trumps or leave it
        max = len(trumpsInHandByGamemode(hand, (3, 0)))
        for solo in validBids:
            if solo[0] == 3:
                trumpsInHand = trumpsInHandByGamemode(hand, solo)
                if len(trumpsInHand) >= 5 and len(trumpsInHand) > max:
                    chosenSolo = solo

    if chosenSolo != (None, None):
        trumpsInHand = trumpsInHandByGamemode(hand, chosenSolo)
        if len(trumpsInHand) >= 6:
            return chosenSolo
        elif len(trumpsInHand) == 5:
            reversed = dict(zip(SUITS.values(), SUITS.keys()))
            if countColourOfSuit(hand, reversed[chosenSolo[1]]) >= 2:
                chosenSolo = (None, None)

    return chosenSolo


# Possibly look at 2U(top 2),2A
def choseWenzGame(validBids, hand):
    uCount = countByRank(hand, 'U')
    aCount = countByRank(hand, 'A')
    ret = (None, None)
    if uCount >= 3:
        if aCount >= 2:
            ret = (2, None)
        elif aCount == 1:
            ace = list(filter(lambda x: x.rank == 'A', hand))[0]
            aceSuitsInHand = countAllSuits(hand)
            if aceSuitsInHand >= 3:
                ret = (2, None)
    return ret


# We are aiming for 6 Tricks and if U<4 UE is necessary
def choseWenzGameRevised(validBids, hand):
    uCount = countByRank(hand, 'U')
    aCount = countByRank(hand, 'A')
    sCount = countAllSuits(hand, ['U'])
    validBid = (None, None)

    # 4 U with A+3 or AA or AT
    if uCount == 4:
        # AAXX
        if aCount >= 2:
            validBid = (2, None)
        elif aCount == 1:
            ace = list(filter(lambda x: x.rank == 'A', hand))[0]
            aceSuitCount = countColourOfSuit(hand, ace.suit, ['U', 'A'])
            # ATXX
            if rankOfSuitInHand(hand, ace.suit, 'T'):
                validBid = (2, None)
            # A2X
            elif aceSuitCount >= 2:
                validBid = (2, None)
    # 3U with UE
    elif uCount == 3:
        if rankOfSuitInHand(hand, 'Eichel', 'U'):
            # UUUAAAXX
            if aCount >= 3:
                validBid = (2, None)
    # 2U with UE
    elif uCount == 2:
        if rankOfSuitInHand(hand, 'Eichel', 'U'):
            # AAAA
            if aCount == 4:
                validBid = (2, None)
            # AAA+T|+3
            elif aCount == 3:
                aces = list(filter(lambda x: x.rank == 'A', hand))
                colours = countAllSuits(hand, ['U', 'A'])
                if any(rankOfSuitInHand(hand, x.suit, 'T') for x in aces) or any(
                        len(colours[SUITS[x.suit]] >= 3) for x in aces):
                    validBid = (2, None)
            # AA+TT|T+2 => UUATAT
            elif aCount == 2:
                aces = list(filter(lambda x: x.rank == 'A', hand))
                tens = [rankOfSuitInHand(hand, x.suit, 'T') for x in aces]  # Checks for T of the same suit as A
                colours = countAllSuits(hand, ['U', 'A'])
                # ATAT
                if sum(tens) >= 2:
                    validBid = (None, None)
                # ATAss e.g UUATAKO
                elif sum(tens) >= 1:
                    #
                    suitsInHand = [getCardsOfSuit(hand, s, ['U']) for s in SUITS]
                    testAT = None
                    testA2 = None
                    for suit in suitsInHand:
                        if rankInHand(suit, 'A') and rankInHand('T'):
                            testAT = True
                            continue
                        if rankInHand(suit, 'A') and len(suit) >= 3:
                            testA2 = True
                        if testA2 and testAT:
                            validBid = (2, None)
                # UUATSSS
                elif aCount == 1:
                    suitsInHand = [getCardsOfSuit(hand, s, ['U']) for s in SUITS]
                    for suit in suitsInHand:
                        if rankInHand(suit, 'A') and rankInHand(suit, 'T') and len(suit) >= 5:
                            validBid = (2, None)
                            break

    return validBid


# Returns a set of Trumps in hand
def trumpsInHandByGamemode(hand, gameMode):
    trumps = createTrumps(gameMode)
    trumpsInHand = set(hand) & trumps
    return trumpsInHand


# Returns count of Rank
def countByRank(hand, rank):
    count = 0
    for card in hand:
        if card.rank == rank:
            count += 1
    return count


# Returns either a count of A,T,9,8,7 for all colours as list [E,G,H,S]
def countAllSuits(hand, ignore=['O', 'U']):
    counts = [0, 0, 0, 0]
    for card in hand:
        if card.rank not in ignore:
            counts[SUITS[card.suit]] += 1
    return counts

# Returns count for certain suit in hand with ignore[]
def countColourOfSuit(hand, suit, ignore=['O', 'U', 'A']):
    count = 0
    for card in hand:
        if card.suit == suit and card.rank not in ignore:
            count += 1
    return count


# BOOL:Returns True if Card in hand
def rankOfSuitInHand(hand, suit, rank):
    card = Card(suit, rank)
    return card in hand


# BOOL:Returns True if any card with Rank in hand
def rankInHand(hand, rank):
    for card in hand:
        if rank == card.rank:
            return True
    return False


# BOOL:Returns cards of Suit and Ignore as list in hand
def getCardsOfSuit(hand, suit, ignore=[]):
    cards = list(filter(lambda x: x.suit == suit and x.rank not in ignore, hand))
    return cards
