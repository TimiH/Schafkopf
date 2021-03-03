from helper import createTrumps
from CardValues import RANKS, SUITS

#Returns best TeamGame or (None,None) if no gamemode possible or sensible
def choseTeamGame(validBids, hand):
    possibleTeam = list(filter(lambda x: x[0] == 1, validBids))
    ret = (None, None)
    if not possibleTeam:
        return (None, None)

    #Counting U,O,T,A and
    uCount = countCardInHand(hand,'U')
    oCount = countCardInHand(hand,'O')
    tCount = int(len(trumpsInHandByGamemode(hand,(1,))))
    aCount = countCardInHand(hand,'A')
    colourCount = countColoursInHand(hand) #Counts[E,G,H,S]
    total = uCount + oCount + tCount
    print('Total: '+str(total),'Ober: ' +str(oCount),' Unter:' + str(uCount), ' #Asse:' + str(aCount))

    # Decide if possible otherwise delete list
    #6 Trump or better
    if total >= 6:
        print('Option 6 Trump')
        pass
    #5 Trump
    elif total == 5:
        #1 colour missing/Ace
        if any(x.rank == 'A' and x.suit != 'Herz' for x in hand) or any(colourCount[x] == 0 for x in [0,1,3]):
            print('Option 5 Trump: Fehl or Ace')
            pass
        #2O & U
        elif oCount >= 2 and uCount <= 1:
            print('Option 5 Trump: 2O&1U')
            pass
    #4 Trump containing 1 out of [OE,OG,OH], 1 U, and two Aces not heart
    elif total ==4:
        if oCount == 1 and uCount == 1 and any(x.rank == 'O' and x.suit in ['Eichel', 'Gras', 'Herz'] for x in hand):
            #two non trump aces
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
            if countSpatzenOfSuit(hand, reversed[chosenSolo[1]]) >= 2:
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


def choseWenzGame2(validBids, hand):
    pass

# Returns a set of Trumps in hand
def trumpsInHandByGamemode(hand, gameMode):
    trumps = createTrumps(gameMode)
    trumpsInHand = set(hand) & trumps
    return trumpsInHand

# Returns count of Rank
def countCardInHand(hand, rank):
    count = 0
    for card in hand:
        if card.rank == rank:
            count += 1
    return count

# Returns either a count of A,T,9,8,7 for all colours as list [E,G,H,S]
def countColoursInHand(hand):
    counts = [0, 0, 0, 0]
    for card in hand:
        if card.rank not in ['U', 'O']:
            counts[SUITS[card.suit]] += 1
    return counts


# Returns count of A,T,9,8,7 for all colour
def countColourOfSuit(hand,colour):
    count = 0
    for card in hand:
        if card.suit == colour and card.rank not in ['U', 'O']:
            count += 1
    return count

#Count T,9,8,7 of suir
def countSpatzenOfSuit(hand, suit):
    count = 0
    for card in hand:
        if card.rank not in ['O','U','A'] and card.suit != suit:
            count += 1
    return count
