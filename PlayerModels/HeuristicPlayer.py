from Player import Player
from PlayerModels.staticBidding import choseSoloGame, choseWenzGameRevised, choseTeamGame

__metaclass__ = type


class HeuristicPlayer(Player):
    def makeBid(self, validBids):
        teamGameChoice = choseTeamGame(validBids, self.hand)
        wenzGameChoice = choseWenzGameRevised(self.hand)
        soloGameChoice = choseSoloGame(validBids, self.hand)
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
        # print((max, self.hand))
        return max

        def playCard(self, validCards, gameDict, trickHistory):
            if len(validCards) == 1:
                return validCards[0]
            mode, _ = gameDict['GameMode']
            if mode == 1:
                card = playTeamCard(validCards, gameDict, trickHistory)
            if mode == 2:
                card = playWenzCard(validCards, gameDict, trickHistory)
            if mode == 3:
                card = playSoloCard(validCards, gameDict, trickHistory)
            return card

        def playTeamCard(self, validCards, gameDict, trickHistory):
            pass

        def playSoloCard(self, validCards, gameDict, trickHistory):
            pass

        def playWenzCard(self, validCards, gameDict, trickHistory):
            # Decide Player or Opposition
            if self.position == gameDict['offensivePlayers'][0]:
                # Lead
                if len(trickHistory) == 0:
                    pass
                # noLead
                else:

                pass
            # Opposition
            else:
                pass
