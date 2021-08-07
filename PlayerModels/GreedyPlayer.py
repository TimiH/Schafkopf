from PlayerModels.Player import Player
from PlayerModels.staticBidding import choseSoloGame, choseWenzGameRevised, choseTeamGame, choseWenzGameSimple

from PlayerModels.staticBidding import getCardsOfRank, cardInHand, getCardOfSuitRank, \
    trumpsInHandByGamemode, getCardsOfSuit
from helper import createTrumpsList, byRank, getTrickWinnerIndex, sumTrickHistory, ringTest, sortTrump, getParnterPos, \
    getValidWinners


class GreedyPlayer(Player):
    def makeBid(self, validBids):
        teamGameChoice = choseTeamGame(validBids, self.hand)
        wenzGameChoice = choseWenzGameSimple(self.hand)
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
        # if max != (0, 0):
        #     print((max, self.hand))
        return max

    def playCard(self, validCards, gameDict, trickHistory):
        if len(validCards) == 1:
            return validCards[0]

        gameMode = gameDict['gameMode']
        trumps = createTrumpsList(gameMode)
        # Lead play highest Card
        if len(trickHistory) == 0:
            # play highest Card
            validNoTrump = list(set(validCards) - set(trumps))
            if validNoTrump:
                card = min(validNoTrump, key=byRank)
            else:
                trumpInHand = trumpsInHandByGamemode(validCards, gameMode)
                orderedTrump = sortTrump(trumpInHand)
                card = orderedTrump[0]
        else:
            # win or min
            winningCards = getValidWinners(trickHistory, validCards, gameMode)
            if winningCards:
                card = max(winningCards, key=lambda x: x[1])[0]
            else:
                validNoTrump = list(set(validCards) - set(trumps))
                if validNoTrump:
                    card = min(validNoTrump, key=lambda x: x.value)
                else:
                    card = min(validCards, key=lambda x: x.value)
        if not card:
            raise Exception
        return card
