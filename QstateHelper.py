from bitarray import bitarray
from CardValues import RANKS, SUITS
# self.players = gameDict['players']  # List of players and Positons via index
#             self.playersHands = gameDict['playersHand']
#             self.scores = gameDict['scores']
#             self.leadingPlayer = gameDict['leadingPlayer']
#             self.history = gameDict['history']
#             self.cardsPlayed = gameDict['cardsPlayed']
#
#             self.gameMode = gameDict['gameMode']
#             self.bids = gameDict['bids']
#             self.offensivePlayers = gameDict['offensivePlayers']
#             self.runAwayPossible = gameDict['runAwayPossible']
#
#             self.currentTrick = gameDict['currentTrick']
#             self.ranAway = gameDict['ranAway']
#             self.searched = gameDict['searched']
#             self.laufende = gameDict['laufende']
#
#             self.rewards = gameDict['rewards']
#             self.trumpCards = gameDict['trumpCards']
#
#             self.seed = gameDict['seed']

def Qstates(hand, validCards, playedCard,gameDict,trickhistory):
    qstateDict = {}
    trueVector = getTrueVector()
    # Card Related
    qstateDict['Hand'] = createBitArrayFromHand(hand)
    qstateDict['ValidCards'] = createBitArrayFromHand(validCards)
    qstateDict['playedCards'] = createBitArrayFromCard(playedCard)
    qstateDict['Trumps'] = createBitArrayFromHand(gameDict['trumpCards'])
    qstateDict['TrumpsRemainOthers'] =  qstateDict['Trumps'] & ~qstateDict['playedCards'] &~qstateDict['Hand']
    qstateDict['CardsLeftInGameOthers'] = trueVector & ~qstateDict['playedCards'] &~qstateDict['Hand']

    #Trickrelated
    qstateDict['TrickPos'] = ''
    qstateDict['CurrentWinnerPos'] = ''
    qstateDict['Lead'] = gameDict[]
    #General Game
    qstateDict['teamScores'] = ''
    qstateDict['pointsLeftInGame'] = ''
    qstateDict['ranAway'] = gameDict['ranAway']
    #TODO does it if we are 2 and 1 searched?
    qstateDict['searched'] = gameDict['searched']
    #TODO what do we need player
    qstateDict['PostionMeTable'] =
    qstateDict['GameMode'] =
    qstateDict['OwnTeam'] =
    
    return qstateDict

def createBitArrayFromHand(hand):
    array = bitarray(32)
    array.setall(0)
    for card in hand:
        index = SUITS[card.suit] * 8 + RANKS.index(card.rank)
        array[index] = 1
    return array

def createBitArrayFromCard(card):
    array = bitarray(32)
    array.setall(0)
    index = SUITS[card.suit] * 8 + RANKS.index(card.rank)
    array[index] = 1
    return array

def getTrueVector():
    a = bitarray(32)
    a.setall(1)
    return a

def aMinusB(a,b):
    return a & ~b