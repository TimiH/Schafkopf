from operator import itemgetter
from Player import Player
from helper import sortHand
from staticBidding import choseSoloGame, choseTeamGame, choseWenzGame, choseWenzGameRevised
import random

__metaclass__ = type

class RandomPlayer(Player):
    def __init__(self, name):
        self.name = name
        self.hand = []

    def setHand(self, cards):
        self.hand = sortHand(cards)

    # Somewhat adopted from https://github.com/Taschee/schafkopf/blob/master/schafkopf/players/heuristics_player.py
    def makeBid(self, validBids):
        teamGameChoice = choseTeamGame(validBids,self.hand)
        wenzGameChoice = choseWenzGameRevised(self.hand)
        soloGameChoice = choseSoloGame(validBids,self.hand)
        bids = []

        max = (None, None)
        if teamGameChoice[0] > max[0]:
            max = teamGameChoice
        if wenzGameChoice[0] > max[0]:
            max = wenzGameChoice
        if soloGameChoice[0] > max[0]:
            max = soloGameChoice
        # print("PLAYERCHOICES",max,teamGameChoice,wenzGameChoice,soloGameChoice)
        if max != (None, None): print(max, self.hand)
        return max

    def playCard(self, validCards, state, trickHistory):
        card = random.choice(validCards)
        # print(self.name, validCards)
        # self.hand.remove(card)
        # print("{} plays {} and has left {}").format(self.name,card, self.hand)
        # print("{} ->:{}".format(self.name,card))
        return card
