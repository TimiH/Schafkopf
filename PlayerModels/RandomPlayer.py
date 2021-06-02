from operator import itemgetter
from Player import Player
from helper import sortHand
from .staticBidding import choseSoloGame, choseTeamGame, choseWenzGame, choseWenzGameRevised
import random

__metaclass__ = type

class RandomPlayer(Player):
    # Somewhat adopted from https://github.com/Taschee/schafkopf/blob/master/schafkopf/players/heuristics_player.py
    def makeBid(self, validBids):
        teamGameChoice = choseTeamGame(validBids,self.hand)
        wenzGameChoice = choseWenzGameRevised(self.hand)
        soloGameChoice = choseSoloGame(validBids,self.hand)
        bids = []

        max = (0, 0)
        if teamGameChoice[0] > max[0]:
            max = teamGameChoice
        if wenzGameChoice[0] > max[0]:
            max = wenzGameChoice
        if soloGameChoice[0] > max[0]:
            max = soloGameChoice
        # print("PLAYERCHOICES",max,teamGameChoice,wenzGameChoice,soloGameChoice)
        if max != (0, 0):
            print((max, self.hand))
        return max

    # reateQstates(hand, validCards, playedCard, position, gameDict, trickhistory):
    def playCard(self, validCards, gameDict, trickHistory):
        card = random.choice(validCards)
        if self.record:
            self.recordQstate(self.hand, validCards, card, gameDict, trickHistory)
        return card
