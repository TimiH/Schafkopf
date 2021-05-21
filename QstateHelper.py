from bitarray import bitarray
from CardValues import RANKS, SUITS


def createQstates(hand, validCards, playedCard, position, gameDict, trickhistory):
    qstateDict = {}
    trueVector = getTrueVector()
    # Card Related all are 32bit Array
    qstateDict['uuid'] = gameDict['uuid']
    qstateDict['Hand'] = createBitArrayFromHand(hand)
    qstateDict['ValidCards'] = createBitArrayFromHand(validCards)
    qstateDict['playedCards'] = createBitArrayFromCard(playedCard)
    qstateDict['Trumps'] = createBitArrayFromHand(gameDict['trumpCards'])
    qstateDict['TrickHistory'] = createBitArrayFromHand(trickhistory)
    qstateDict['TrumpsRemainOthers'] = qstateDict['Trumps'] & ~qstateDict['playedCards'] & ~qstateDict['Hand'] & ~ \
        qstateDict['TrickHistory']
    qstateDict['CardsLeftInGameOthers'] = trueVector & ~qstateDict['playedCards'] & ~qstateDict['Hand']

    # Trickrelated all are 4bit Array
    qstateDict['TrickPos'] = createTrickPosition(trickhistory)
    # qstateDict['CurrentWinnerPos'] = ''
    qstateDict['Lead'] = createPositionArrayFromIndex(gameDict['leadingPlayer'])
    # General Game
    qstateDict['Score0'] = gameDict['scores'][0]
    qstateDict['Score1'] = gameDict['scores'][1]
    qstateDict['Score2'] = gameDict['scores'][2]
    qstateDict['Score3'] = gameDict['scores'][3]
    qstateDict['pointsLeftInGame'] = 120 - sum(gameDict['scores'])
    qstateDict['pointsInTrick'] = collectPointsInTrick(trickhistory)
    qstateDict['ranAway'] = gameDict['ranAway']
    qstateDict['searched'] = gameDict['searched']
    qstateDict['PostionMeTable'] = createPositionArrayFromIndex(position)
    qstateDict['GameMode'] = gameDict['gameMode']
    qstateDict['OwnTeam'] = createTeamArray(position, gameDict)
    qstateDict['teamScores'] = createTeamScores(gameDict['scores'], [qstateDict['OwnTeam']])

    return qstateDict


def createBitArrayFromHand(hand):
    array = bitarray(32)
    array.setall(0)
    for card in hand:
        index = SUITS[card.suit] * 8 + RANKS.index(card.rank)
        array[index] = 1
    return array


def createBitArrayFromCard(card):
    array = createFalseArray(32)
    index = SUITS[card.suit] * 8 + RANKS.index(card.rank)
    array[index] = 1
    return array


def getTrueVector():
    a = bitarray(32)
    a.setall(1)
    return a


def createTrickPosition(trickhistory):
    index = len(trickhistory)
    array = createFalseArray(4)
    array[index] = 1
    return array


# Returns 4bit array with index, 0-> 1000,1 -> 0100
def createPositionArrayFromIndex(index):
    array = bitarray(4)
    array.setall(0)
    array[index] = 1
    return array


def createTeamScores(scoreList, teamArray):
    teamScore = 0
    for count, value in enumerate(teamArray):
        if value == 1:
            teamScore = teamScore + scoreList[count]
    return teamScore


def createFalseArray(length):
    array = bitarray(length)
    array.setall(0)
    return array


def createTeamArray(position, gameDict):
    gameMode, suit = gameDict['gameMode']
    bidWinner = gameDict['offensivePlayers'][0]
    array = createFalseArray(4)
    for i in gameDict['offensivePlayers']:
        array[i] = 1
    # TeamGame
    if gameMode == 1:
        # OffensiveSide?
        if position in gameDict['offensivePlayers']:
            # Offense and teams are public
            if gameDict['ranAway'] or gameDict['searched']:
                return array
            else:
                # Mitspieler knows everything
                if position == gameDict['offensivePlayers'][1]:
                    return array
                # bidWinner knows nothing
                else:
                    array.setall(0)
                    array[position] = 1
                    return array
        # opposition Team
        else:
            if gameDict['ranAway'] or gameDict['searched']:
                return ~array
            else:
                array.setall(0)
                array[position] = 1
                return array
    # Wenz/Solo
    else:
        if position in gameDict['offensivePlayers']:
            return array
        else:
            return ~array


def collectPointsInTrick(trickhistory):
    points = 0
    for card in trickhistory:
        points += card.value
    return points


def convertBitArraysInDictTo01(qstates):
    for key in qstates.keys():
        if isinstance(qstates[key], bitarray):
            qstates[key] = qstates[key].to01()
