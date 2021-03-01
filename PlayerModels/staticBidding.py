from helper import createTrumps
from CardValues import RANKS, SUITS

def choseTeamGame(validBids, hand):
    possibleTeam = list(filter(lambda x: x[0] == 1, validBids))
    ret = (None, None)
    if not possibleTeam:
        return (None, None)

    uCount = countCardInHand(hand,'U')
    oCount = countCardInHand(hand,'O')
    tCount = countColoursInHand(hand,'Herz')
    aCount = countCardInHand(hand,'A')
    colourCount = countColoursInHand(hand)
    total = uCount + oCount + tCount
    # Decide if possible otherwise delete list
    if total >= 4 and oCount >= 1 and uCount >= 1 and aCount >= 2 and any(
            x.rank == 'O' and x.rank in ['Eichel', 'Gras', 'Herz'] for x in hand):
        pass
    elif total >= 5 and oCount >= 2 and uCount >= 1 and all(x > 0 for x in colourCount):
        pass
    elif total >= 5 and (colourCount[0] == 0 or colourCount[1] == 0 or colourCount[3] == 0):
        pass
    elif total >= 6:
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
    uCount = countCardInHand(hand, 'U')
    oCount = countCardInHand(hand, 'O')
    chosenSolo = (None, None)
    if (uCount + oCount) < 3:
        return chosenSolo
    else:
        # Find the solo with the most trumps or leave it
        max = len(trumpsInHandByGamemode(hand,(3, 0)))
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
            if countSpatzenForTrump(hand, reversed[chosenSolo[1]]) >= 2:
                chosenSolo = (None, None)

    return chosenSolo


# Possibly look at 2U(top 2),2A
def choseWenzGame(validBids, hand):
    uCount = countCardInHand(hand, 'U')
    aCount = countCardInHand(hand, 'A')
    ret = (None, None)
    if uCount >= 3:
        if aCount >= 2:
            ret = (2, None)
        elif aCount == 1:
            ace = list(filter(lambda x: x.rank == 'A', hand))[0]
            aceSuitsInHand = countColoursInHand(hand, ace.suit)
            if aceSuitsInHand >= 3:
                ret = (2, None)
    return ret


def trumpsInHandByGamemode(hand, gameMode):
    trumps = createTrumps(gameMode)
    trumpsInHand = set(hand) & trumps
    return trumpsInHand


def countCardInHand(hand, rank):
    count = 0
    for card in hand:
        if card.rank == rank:
            count += 1
    return count


# Returns either a count for all colours as list [E,G,H,S] or count for specific colour
def countColoursInHand(hand, colour=None):
    counts = [0, 0, 0, 0]
    if colour == None:
        for card in hand:
            if card.rank not in ['U', 'O']:
                counts[SUITS[card.suit]] += 1
        return counts
    else:
        count = 0
        for card in hand:
            if card.suit == colour and card.rank not in ['U', 'O']:
                count += 1
        return count

#TODO
def countSpatzenForTrump(hand, suit):
    count = 0
    for card in hand:
        if card.rank != 'A' and card.suit != suit:
            count += 1
    return count
