from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer
# from random import
from copy import deepcopy,copy
from Deck import Deck

class RSamplerMaster:
    def __init__(self, validCards, hand, position, gamesDict, trickHistory, ):
        # carriedOver
        self.masterCopy = gamesDict
        self.validCards = validCards
        self.position = position
        self.trickHistory = trickHistory
        self.hand = hand
        self.gameMode = gamesDict['gameMode']
        # Own variables
        self.nodes = []
        self.result = None
        self.scores = None
        self.points = None
        self.teamsKnown = self.teamsKnown()
        self.remainingCards = self.getRemainingCards()
        self.playerHands = self.fillPlayerHands()
        self.currentTrick = len(gamesDict['histoy'])

    def createNodes(self):
        pass

    def getRemainingCards(self):
        deck = set(Deck().cards)
        hand = set(deepcopy(self.hand))
        cardsPlayed = set(deepcopy(self.gameDict['cardsPlayed']))
        trickHistory = set(deepcopy(self.trickHistory))
        availableCards = deck - hand - cardsPlayed - trickHistory
        return list(availableCards)

    def fillPlayerHands(self):
        #fill current trick to playerHands
        hands = [[],[],[],[]]
        lead = self.masterCopy['leadingPlayer']
        for key,card in enumerate(self.trickHistory):
            c = copy(card)
            self.playerHands[key+lead].append(c)
        if self.gameMode == 1:
            if self.teamsKnown():
        else:
            return


    def teamsKnown(self):
        if self.masterCopy['searched'] or ['ranAway']:
            return True
        else:
            return False

    def evaluate(self):
        pass

    def returnCard(self):
        pass


class RSamplerNode(object):
    def __init__(self, gamestate, card, availableCards, lenHands, simRuns=100, simTime=2):
        pass

    def runSim(self):
        pass

    def distributeCards(self):
        pass

    def hashCards(self):
        pass
