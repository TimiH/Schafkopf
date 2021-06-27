import random

from Player import Player
from PlayerModels.staticBidding import choseSoloGame, choseWenzGameRevised, choseTeamGame
from PlayerModels.staticBidding import getCardsOfRank
from helper import createTrumpsList, byRank, getTrickWinnerIndex, sumTrickHistory
from copy import copy

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
        card = None
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
        card = None
        if self.position == gameDict['offensivePlayers'][0]:
            # Lead
            if len(trickHistory) == 0:
                # Play U until we have superiority
                playedU = getCardsOfRank(gameDict['cardsPlayed'], 'U')
                uHand = getCardsOfRank(validCards)
                trumplist = createTrumpsList((2, 0))
                oppositionU = set(trumplist) - set(playedU) - set(uHand)
                if len(oppositionU) != 0 and len(uHand) > 0:
                    card = min(uHand)
                else:
                    # we have trump control or no trump
                    # playhighest Rank
                    validNoU = [x for x in validCards if x.rank != 'U']
                    if validNoU:
                        card = min(validCards)
                if not card:
                    return random.choice(validCards)
            # noLead
            else:
                trickPosIndex = len(trickHistory)
                # can we trick
                winningCards = []
                # test cards if winning and append (card,trickscore)
                for c in validCards:
                    testTrickHistory = copy(trickHistory)
                    testTrickHistory.append(c)
                    winningIndex = getTrickWinnerIndex(trickHistory, (2, 0))
                    if winningIndex == trickPosIndex:
                        winningCards.append((c, sumTrickHistory(testTrickHistory)))
                if winningCards:
                    # choose card that max scores
                    card = max(winningCards, key=lambda x: x[1])[0]
                else:
                    # use card with least value and not U
                    validNoU = [x for x in validCards if x.rank != 'U']
                    if validNoU:
                        card = min(validNoU, key=lambda x: x.value)
                    else:
                        card = random.choice(validCards)
        # Opposition
        else:
            bidWinnerTablePos = gameDict['offensivePlayers'][0]
            trickLead = gameDict['leadingPlayer']
            # Lead
            if len(trickHistory) == 0:
                # Play color Aces
                validNoU = [x for x in validCards if x.rank != 'U']
                if not validNoU:
                    card = random.choice(validCards)
                else:
                    # play Aces if possible
                    aces = getCardsOfRank(validCards, 'A')
                    if aces:
                        card = random.choice(aces)
                    else:
                        # trynotplay naked T
                        validNoUT = [x for x in validCards if x.rank != 'U' and x.rank != 'T']
                        if validNoUT:
                            card = random.choice(aces)
                        else:
                            card = random.choice(validCards)
            # No Lead
            else:
                # Who owns the trick
                currentWinnerTrickPos = getTrickWinnerIndex(trickHistory, (2, 0))
                winningTableIndex = (currentWinnerTrickPos + trickLead) % 4
                # bidWinner owns trick
                if bidWinnerTablePos == winningTableIndex:
                    # test cards if winning and append (card,trickscore)
                    trickPosIndex = len(trickHistory)
                    winningCards = []
                    for c in validCards:
                        testTrickHistory = copy(trickHistory)
                        testTrickHistory.append(c)
                        winningIndex = getTrickWinnerIndex(trickHistory, (2, 0))
                        if winningIndex == trickPosIndex:
                            winningCards.append((c, sumTrickHistory(testTrickHistory)))
                    if winningCards:
                        card = max(winningCards, key=lambda x: x[1])[0]
                    else:
                        # choose lowest card by value not U
                        validNoU = [x for x in validCards if x.rank != 'U']
                        if validNoU:
                            card = min(validNoU, key=lambda x: x.value)
                        else:
                            card = random.choice(validCards)
                # opposition owns trick
                else:
                    # see which cards maximises current score
                    scoringCards = []
                    for c in validCards:
                        testTrickHistory = copy(trickHistory)
                        testTrickHistory.append(c)
                        scoringCards.append((c, sumTrickHistory(testTrickHistory)))
                    card = max(scoringCards, key=lambda x: x.value)[0]
        if card not in validCards:
            print(f'ERROR{card=},{validCards=}')
            return random.choice(validCards)
        else:
            return card
