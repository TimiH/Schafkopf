from PlayerModels.Player import Player
from Deck import Deck
from random import sample
from operator import add
from copy import deepcopy


class RandomSamplePlayer(Player):

    def getAvailableCards(self):
        deck = set(Deck().cards)
        hand = set(deepcopy(self.gameDict['playerHands'][self.playerPosition]))
        cardsPlayed = set(deepcopy(self.gameDict['cardsPlayed']))
        trickHistory = set(deepcopy(self.trickHistory))
        availableCards = deck - hand - cardsPlayed - trickHistory
        return list(availableCards)
