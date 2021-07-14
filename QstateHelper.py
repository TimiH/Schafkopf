import numpy as np
from bitarray import bitarray
from CardValues import RANKS, SUITS
from helper import rotateListBackwards,rotateListForward

def createQstates(hand, validCards, playedCard, position, gameDict, trickhistory):
    qstateDict = {}
    trueVector = getTrueVector()
    # Card Related all are 32bit Array
    qstateDict['uuid'] = gameDict['uuid']
    qstateDict['Hand'] = createBitArrayFromHand(hand)
    qstateDict['ValidCards'] = createBitArrayFromHand(validCards)
    qstateDict['playedCards'] = createBitArrayFromCard(playedCard)
    qstateDict['Trumps'] = createBitArrayFromHand(gameDict['trumpCards'])
    qstateDict['history'] = convertHistory(gameDict['history'],position)
    #TODO split
    qstateDict['TrickHistory'] = trickHistoryToArray(trickhistory,position)

    qstateDict['TrumpsRemainOthers'] = qstateDict['Trumps'] & ~qstateDict['playedCards'] & ~qstateDict['Hand'] & ~ \
        qstateDict['TrickHistory']
    qstateDict['CardsLeftInGameOthers'] = trueVector & ~qstateDict['playedCards'] & ~qstateDict['Hand']

    # Trickrelated all are 4bit Array
    qstateDict['TrickPos'] = createTrickPosition(trickhistory)
    # qstateDict['CurrentWinnerPos'] = ''
    qstateDict['Lead'] = createPositionArrayFromIndex(gameDict['leadingPlayer'])
    # General Game

    #Scores: rotated normalized
    scoresRotated = rotateListBackwards(gameDict['scores'],position)
    qstateDict['Score0'] = scoresRotated[0] / 120
    qstateDict['Score1'] = scoresRotated[0] / 120
    qstateDict['Score2'] = scoresRotated[0] / 120
    qstateDict['Score3'] = scoresRotated[0] / 120

    qstateDict['pointsLeftInGame'] = 120 - sum(gameDict['scores'])/120
    qstateDict['pointsInTrick'] = collectPointsInTrick(trickhistory)/120
    qstateDict['teamScores'] = createTeamScores(gameDict['scores'], [qstateDict['OwnTeam']]) / 120

    #Bool
    qstateDict['ranAway'] = bitarray(([gameDict['ranAway']]))
    qstateDict['searched'] = bitarray([gameDict['searched']])
    #Encoded
    qstateDict['GameMode'] = gameModeBitArray(gameDict['gameMode'])

    qstateDict['BidWinner'] = createPositionArrayFromIndex(gameDict['offensivePlayers'][0])
    qstateDict['OwnTeam'] = createTeamArray(position, gameDict)

    return qstateDict

def convertHistory(history,postion):
    hist = []
    for h in history:
        hist,lead,_ = h
        tmp = []
        for c in hist:
            tmp.append(createBitArrayFromCard(c))
        afterLead = rotateListBackwards(tmp,lead)
        hist.append(afterPos)
    return hist

#returns [bit(32),bit(32),bit(32),bit(32)] with position = arr[0]
def trickHistoryToArray(trickhistory,position):
    arr = [createFalseArray(32) for _ in range(4)]

    for key,card in enumerate(trickhistory):
        temp = createBitArrayFromCard(card)
        arr[key] = temp
    arr = rotateListBackwards(arr,position)
    return arr

#4+1+4, Sau,Wenz,Solo
def gameModeBitArray(gameMode):
    mode, suit = gameMode
    arr = bitarray(11).setall(0)
    if mode == 1:
        arr[0] = 1
        arr[suit+1] = 1
    if mode == 2:
        arr[5] == 1
    if mode == 3:
        arr[6] == 1
        arr[suit+7]
    return arr

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
    for key in list(qstates.keys()):
        if isinstance(qstates[key], bitarray):
            qstates[key] = qstates[key].to01()
