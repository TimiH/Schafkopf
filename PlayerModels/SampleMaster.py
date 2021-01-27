# -*- coding: utf-8 -*-
from PlayerModels.RandomPlayer import RandomPlayer
from Player import Player
from Deck import Deck
from random import sample, seed, shuffle
from operator import add
from helper import ringTest
from copy import deepcopy, copy


class SampleMaster(object):
    def __init__(self, gamestate, validCards, hand, position, trickHistory):
        self.gamestate = gamestate
        self.history = gamestate.history
        self.playerPosition = position
        self.players = []
        self.availableCards = self.getAvailableCards(hand,trickHistory)
        self.lenHands = []
        self.children = []
        #self.trickHistory = trickHistory

        # getting len hands and finding all the players that played a card, since their card haven´t been removed from the main game yet
        for p in self.gamestate.players:
            self.lenHands.append(len(p.hand))

        for n in range(4):
            lead = self.gamestate.currentTrick.leadingPlayer
            numberCardsPlayed = len(trickHistory)
            if ringTest(lead, numberCardsPlayed, n):
                self.lenHands[n] -= 1

        # initialising Players
        for n in range(4):
            p = Player("SampleMaster" + str(n))
            self.players.append(p)

        # Gamestate manipulations
        self.gamestate.currentTrick.history = trickHistory  # Important because we copy at different State in trick
        self.gamestate.players = self.players
        self.gamestate.players[position].setHand(hand)

        # Create Children for each possible Play
        for card in validCards:
            copy = deepcopy(self.gamestate)
            child = TreeNode(copy, card, self.availableCards, self.lenHands)
            self.children.append(child)
            child.runSim()

    # Returns all the possible cards in the other´s players hands
    def getAvailableCards(self, hand,trickHistory):
        remainingcards = Deck().cards
        remainingcards = [x for x in remainingcards if x not in hand]
        remainingcards = [x for x in remainingcards if x not in self.gamestate.cardsPlayed]
        remainingcards = [x for x in remainingcards if x not in trickHistory]

        # Remove also all cards that have been played in the currentTrick
        for card in self.gamestate.currentTrick.history:
            remainingcards.remove(card)
        return remainingcards


class TreeNode(object):
    def __init__(self, gamestate, card, availableCards, lenHands, simRuns=20, simTime=2):
        self.rewards = [0, 0, 0, 0]
        self.card = card
        self.hashedHands = {}
        self.simRuns = simRuns
        self.simTime = simTime
        self.lenHands = lenHands
        self.availableCards = availableCards
        self.gamestate = gamestate
        self.gamestate.currentTrick.history.append(card)

    def runSim(self):
        count = 0
        while count < self.simRuns:
            #print('Count: {} with {}'.format(count, self.card))
            gamecopy = self.gamestate.copy()
            self.distributeCards(gamecopy)
            gamecopy.currentTrick.gameDict = gamecopy
            gamecopy.currentTrick.updatePlayers(gamecopy.players)
            gamecopy.currentTrick.setMembers()

            # for p in range(4):
            #     print(gamecopy.currentTrick.players[p].name, gamecopy.currentTrick.players[p].hand)

            gamecopy.continueGame()
            gamecopy.setRewards()

            self.rewards = map(add, self.rewards, gamecopy.rewards)
            #print(self.card, gamecopy.rewards)
            count += 1
            # clear(gamecopy)

    def distributeCards(self, gamestate):
        availableCardsCopy = deepcopy(self.availableCards)
        shuffle(availableCardsCopy)

        for p in range(4):
            if gamestate.players[p].hand:
                continue
            #Sampling Cards for Players
            sampledCards = []
            for n in range(self.lenHands[p]):
                sampledCards.append(availableCardsCopy.pop())
            gamestate.players[p].setHand(sampledCards)
