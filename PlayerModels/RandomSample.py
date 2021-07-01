from Player import Player
from Deck import Deck
from random import sample
from operator import add
from copy import deepcopy


class MCTS(object):
    def __init__(self, gameDict, validCards, hand, position, trickHistory):
        self.gameDict = gameDict
        self.trickHistory = trickHistory
        self.playerPosition = position
        self.players = []
        self.availableCards = self.getAvailableCards(hand)
        self.lenHands = []
        self.children = []

        # getting len hands #hacky
        for hand in self.gameDict['playersHands']:
            self.lenHands.append(len(hand))

        for n in range(4):
            p = Player("MCTS" + str(n))
            self.players.append(p)

        self.gameDict.players = self.players

        self.gameDict.players[position].setHand(hand)
        for card in validCards:
            copy = self.gameDict
            copy.players[position].hand.remove(card)
            child = TreeNode(copy, card, self.availableCards, self.lenHands, 100, 5)
            self.children.append(child)
            child.runSim()

    def getAvailableCards(self):
        deck = set(Deck().cards)
        hand = set(deepcopy(self.gameDict['playerHands'][self.playerPosition]))
        cardsPlayed = set(deepcopy(self.gameDict['cardsPlayed']))
        trickHistory = set(deepcopy(self.trickHistory))
        availableCards = deck - hand - cardsPlayed - trickHistory
        return list(availableCards)

class TreeNode(object):
    def __init__(self,gamestate,card,availableCards,lenHands,simRuns=100,simTime=2):
        self.rewards = [0,0,0,0]
        self.card = card
        self.hashedHands = {}
        self.simRuns = simRuns
        self.simTime = simTime
        self.lenHands = lenHands
        self.availableCards = availableCards
        self.gamestate = gamestate
        self.gamestate.currentTrick.trickHistory.append(card)
        # print("We are in: ", self.card,"with Players:",self.gamestate.players)
        # for p in self.gamestate.players:
        #     print(p.hand)

    def runSim(self):
        count = 0
        while count != self.simRuns:
            gamecopy = self.gamestate.copy()
            self.distributeCards(gamecopy)
            #print(gamecopy.players)
            gamecopy.currentTrick.gameDict = gamecopy
            gamecopy.currentTrick.updatePlayers(gamecopy.players)
            gamecopy.currentTrick.setMembers()

            gamecopy.continueGame()
            gamecopy.setRewards()

            self.rewards = list(map(add, self.rewards, gamecopy.rewards))
            #print(self.card,gamecopy.rewards)
            count +=1
            #clear(gamecopy)

    def distributeCards(self,gamestate):
        for p in range(4):
            if gamestate.players[p].hand:
                continue
            #print(self.availableCards,self.lenHands[p])
            sampledCards = sample(self.availableCards,self.lenHands[p])
            gamestate.players[p].setHand(sampledCards)
