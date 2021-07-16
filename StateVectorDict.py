from bitarray import bitarray
from CardValues import RANKS, SUITS
from helper import rotateListBackwards, handsFromHistory

'''
CreateVectorDict returns a dictionary with type:bitarray

        hand:32
        valid cards: 32
        playedCards: 32
        trumps : 32
        history : [(32+4)*4]
        trickHistory : [32*4]
        trumpsRemainOthers : 32
        cardsLeftInGameOthers : 32
        trickPos : 4
        lead : 4
        Score[0-3] : int
        pointsLeftInGame : int
        teamScores : int
        ranAway : 1
        searched : 1
        gameMode : 7
        bidWinner : 4
        ownTeam : 4
'''


def createVectorDict(hand, validCards, position, gameDict, trickHistory):
    vectorDict = {}
    trueVector = getTrueVector()
    # Card Related all are 32bit Array
    vectorDict['uuid'] = gameDict['uuid']
    vectorDict['hand'] = createBitArrayFromHand(hand)
    vectorDict['validCards'] = createBitArrayFromHand(validCards)
    # vectorDict['playedCard'] = createBitArrayFromCard(playedCard)
    vectorDict['trumps'] = createBitArrayFromHand(gameDict['trumpCards'])
    vectorDict['history'] = convertHistory(gameDict['history'], position)
    vectorDict['trickHistoryPlayer'] = trickHistoryArray(trickHistory, position)
    vectorDict['cardsPlayed'] = createBitArrayFromHand(gameDict['cardsPlayed'])
    vectorDict['trickHistory'] = createBitArrayFromHand(trickHistory)
    vectorDict['trumpsRemainOthers'] = vectorDict['trumps'] & ~vectorDict['cardsPlayed'] & ~vectorDict['hand'] & ~ \
        vectorDict['trickHistory']
    vectorDict['cardsLeftInGameOthers'] = trueVector & ~vectorDict['cardsPlayed'] & ~vectorDict['hand']

    # Trick related all are 4bit Array
    vectorDict['trickPos'] = createTrickPosition(trickHistory)
    # vectorDict['CurrentWinnerPos'] = ''
    vectorDict['lead'] = rotateListBackwards(createPositionArrayFromIndex(gameDict['leadingPlayer']), position)

    # General Game
    # Scores: rotated normalized
    scoresRotated = rotateListBackwards(gameDict['scores'], position)
    vectorDict['scores'] = scoresRotated
    vectorDict['score0'] = scoresRotated[0]
    vectorDict['score1'] = scoresRotated[0]
    vectorDict['score2'] = scoresRotated[0]
    vectorDict['score3'] = scoresRotated[0]

    vectorDict['pointsLeftInGame'] = 120 - sum(gameDict['scores'])
    vectorDict['pointsInTrick'] = collectPointsInTrick(trickHistory)
    vectorDict['ownTeam'] = createTeamArray(gameDict, position)
    vectorDict['teamScores'] = createTeamScores(gameDict['scores'], [vectorDict['ownTeam']])

    # Bool
    vectorDict['ranAway'] = bitarray(([gameDict['ranAway']]))
    vectorDict['searched'] = bitarray([gameDict['searched']])
    # Encoded
    vectorDict['gameMode'] = gameModeBitArray(gameDict['gameMode'])
    bidWinner = createPositionArrayFromIndex(gameDict['offensivePlayers'][0])
    vectorDict['bidWinner'] = rotateListBackwards(bidWinner, position)

    return vectorDict


# Returs (32+4)*4
def convertHistory(history, position):
    hands = handsFromHistory(history)
    handsRotated = rotateListBackwards(hands, position)
    arr = []
    for key, hand in enumerate(handsRotated):
        posArray = createPositionArrayFromIndex(key)
        handArray = createBitArrayFromHand(hand)
        arr.append(handArray + posArray)
    return arr


# returns [bit(32),bit(32),bit(32),bit(32)] with position = arr[0]
def trickHistoryArray(trickHistory, position):
    arr = [createFalseArray(32) for _ in range(4)]
    for key, card in enumerate(trickHistory):
        temp = createBitArrayFromCard(card)
        arr[key] = temp
    arr = rotateListBackwards(arr, position)
    return arr


#1+1+1+4, Sau,Wenz,Solo,Color
def gameModeBitArray(gameMode):
    mode, suit = gameMode
    arr = bitarray(7)
    arr.setall(0)
    arr[mode - 1] = 1
    if mode != 2:
        arr[suit + 3] = 1
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


def createTrickPosition(trickHistory):
    index = len(trickHistory)
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


# 4bit
def createTeamArray(gameDict, position):
    arr = createFalseArray(4)
    gameMode, _ = gameDict['gameMode']
    offensivePlayers = gameDict['offensivePlayers']
    for i in offensivePlayers:
        arr[i] = 1
    if position not in offensivePlayers:
        arr = ~arr
    if gameMode != 1:
        arr = rotateListBackwards(arr, position)
    else:
        if position != offensivePlayers[1]:
            if gameDict['searched'] or gameDict['ranAway']:
                arr = rotateListBackwards(arr, position)
            else:
                arr = createFalseArray(4)
                arr[0] = 1
    return arr


def collectPointsInTrick(trickHistory):
    points = 0
    for card in trickHistory:
        points += card.value
    return points


# needed for pickle
def convertBitArraysInDictTo01(vectorDict):
    for key in list(vectorDict.keys()):
        if isinstance(vectorDict[key], bitarray):
            vectorDict[key] = vectorDict[key].to01()
