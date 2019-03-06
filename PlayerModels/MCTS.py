from PlayerModels.RandomPlayer import RandomPlayer
from Deck import Deck
from random import random

class MCTS(object):
    def __init__(self,gamestate,validCards,hand,position):
        self.gamestate = gamestate
        self.history = gamestate.history
        self.playerPosition = position
        self.players = []
        self.availableCards = self.getAvailableCards(hand)
        self.lenHands = []
        self.children = []

        #getting len hands
        for p in self.gamestate.players:
            self.lenHands.append(len(p.hand))

        for n in range(4):
            p = RandomPlayer("MCTS "+str(n))
            self.players.append(p)

        self.gamestate.players = self.players
        self.gamestate.players[position].setHand(hand)
        for card in validCards:
            copy = self.gamestate.copy()
            copy.players[position].hand.remove(card)
            child = TreeNode(copy,card,self.availableCards,self.lenHands,100,5)
            self.children.append(child)
            child.runSim()

    def getAvailableCards(self,hand):
        remainingcards = Deck().cards
        remainingcards = [x for x in remainingcards if x not in hand]
        for trick in self.gamestate.history:
            for card in trick:
                remainingcards -= card
        return remainingcards

class TreeNode(object):
    def __init__(self,gamestate,card,availableCards,lenHands,simRuns=100,simTime=2):
        self.rewards = [0,0,0,0]
        self.hashedHands = {}
        self.simRuns = simRuns
        self.simTime = simTime
        self.lenHands = lenHands
        self.availableCards = availableCards
        self.gamestate = gamestate
        self.gamestate.currentTrick.history.append(card)

    def runSim():
        count = 0
        while count != self.simRuns:
            copy = self.gamestate.copy()
            self.distributeCards(copy)
            copy.continueGame()
            self.rewards = map(add,self.rewards,copy.rewards)
            count +=1
            copy.clear()

    def distributeCards(gamestate):
        for p in range(4):
            if gamestate.players[p].hand:
                continue
            sampledCards = random.sample(self.lenHands[p],self.availableCards)
            self.gamestate.players[p].setHand(sampledCards)
