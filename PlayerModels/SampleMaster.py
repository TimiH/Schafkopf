# -*- coding: utf-8 -*-
from PlayerModels.RandomPlayer import RandomPlayer
from Player import Player
from Deck import Deck
from random import sample, seed, shuffle
from operator import add
from helper import ringTest
from copy import deepcopy, copy


class SampleMaster(object):
    def __init__(self, gamestate, validCards, hand, position):
        self.gamestate = gamestate
        self.history = gamestate.history
        self.playerPosition = position
        self.players = []
        self.availableCards = self.getAvailableCards(hand)
        self.lenHands = []
        self.children = []

        # getting len hands and finding all the players that played a card, since their card haven´t been removed from the main game yet

        for p in self.gamestate.players:
            print(p.hand)
            self.lenHands.append(len(p.hand))
        for n in range(4):
            lead = self.gamestate.currentTrick.leadingPlayer
            numberCardsPlayed = len(self.gamestate.currentTrick.history)
            if ringTest(lead, numberCardsPlayed, n):
                self.lenHands[n] -= 1
        print(self.lenHands)

        # initialising Players
        for n in range(4):
            p = Player("SampleMaster" + str(n))
            self.players.append(p)

        self.gamestate.players = self.players

        self.gamestate.players[position].setHand(hand)
        for card in validCards:
            copy = self.gamestate.copy()
            # copy.players[position].hand.remove(card)
            child = TreeNode(copy, card, self.availableCards, self.lenHands, 10, 5)
            self.children.append(child)
            child.runSim()

    # Returns all the possible cards in the other´s players hands
    def getAvailableCards(self, hand):
        remainingcards = Deck().cards
        remainingcards = [x for x in remainingcards if x not in hand]
        remainingcards = [x for x in remainingcards if x not in self.gamestate.cardsPlayed]
        # for card in self.gamestate.cardsPlayed:
        #     remainingcards.remove(card)

        # Remove also all cards that have been played in the currentTrick
        for card in self.gamestate.currentTrick.history:
            remainingcards.remove(card)
        return remainingcards


class TreeNode(object):
    def __init__(self, gamestate, card, availableCards, lenHands, simRuns=1, simTime=2):
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
        print("we Played: ", self.card)
        count = 0
        while count != self.simRuns:
            gamecopy = self.gamestate.copy()
            self.distributeCards(gamecopy)
            gamecopy.currentTrick.gamestate = gamecopy
            gamecopy.currentTrick.updatePlayers(gamecopy.players)
            gamecopy.currentTrick.setMembers()
            #TODO: REMOVE after debug
            print('------------------------------')
            for p in range(4):
                print(gamecopy.currentTrick.players[p].name, gamecopy.currentTrick.players[p].hand)

            gamecopy.continueGame()
            gamecopy.setRewards()

            self.rewards = map(add, self.rewards, gamecopy.rewards)
            print(self.card,gamecopy.rewards)
            count += 1
            # clear(gamecopy)

    def distributeCards(self, gamestate):
        seed(1)
        availableCardsCopy = deepcopy(self.availableCards)
        shuffle(availableCardsCopy)
        print('------------------\nDISTRIBUTECARDS')
        #All hands beside own hand are empty
        for p in range(4):
            if gamestate.players[p].hand:
                continue

            sampledCards = []
            for n in range(self.lenHands[p]):
                sampledCards.append(availableCardsCopy.pop())
            gamestate.players[p].setHand(sampledCards)