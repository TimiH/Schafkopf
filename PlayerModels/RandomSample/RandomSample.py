from helper import createTrumps
from CardValues import SUITS
from Player import Player
from PlayerModels.RandomSample.SampleMaster import SampleMaster
from PlayerModels.staticBidding import choseSoloGame, choseTeamGame, choseWenzGameRevised

__metaclass__ = type


class RandomSample(Player):

    def playCard(self, validCards, gamestate, trickHistory):
        # If no cards or 1 card
        if len(validCards) == 1:
            return validCards[0]
        else:
            position = self.getPosition(gamestate)
            # print("--------------------------------")
            # print("SampleMaster Position",position)
            masternode = SampleMaster(gamestate, validCards, self.hand, position, trickHistory)
            scoreArray = []
            for child in masternode.children:
                print("TreeNode:", child.card, child.rewards, masternode.playerPosition)
                scoreArray.append(child.rewards[position])
            best = max(scoreArray)
            bestIndex = scoreArray.index(best)
            card = masternode.children[bestIndex].card
            print("Playing:{}".format(card))
            # print("Hand:{},Playing: {},validCards: {}".format(self.hand,card,validCards))
            # self.hand.remove(card)
            return card

    # Somewhat adopted from https://github.com/Taschee/schafkopf/blob/master/schafkopf/players/heuristics_player.py
    def makeBid(self, validBids):
        teamGameChoice = choseTeamGame(validBids, self.hand)
        wenzGameChoice = choseWenzGameRevised(self.hand)
        soloGameChoice = choseSoloGame(validBids, self.hand)
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
