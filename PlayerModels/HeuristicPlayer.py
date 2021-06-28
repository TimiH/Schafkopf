import random

from Player import Player
from PlayerModels.staticBidding import choseSoloGame, choseWenzGameRevised, choseTeamGame, choseWenzGame
from PlayerModels.staticBidding import getCardsOfRank, cardInHand, rankInHand, getCardOfSuitRank
from helper import createTrumpsList, byRank, getTrickWinnerIndex, sumTrickHistory, ringTest
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
            print((max, self.hand))
        return max

    def playCard(self, validCards, gameDict, trickHistory):
        if len(validCards) == 1:
            # print(f'Only:{self.position, validCards, trickHistory, validCards[0]}')
            return validCards[0]
        mode, _ = gameDict['gameMode']
        card = None
        if mode == 1:
            card = self.playTeamCard(validCards, gameDict, trickHistory)
        if mode == 2:
            card = self.playWenzCard(validCards, gameDict, trickHistory)
        if mode == 3:
            card = self.playSoloCard(validCards, gameDict, trickHistory)
        # print('---------------')
        # print(f'{self.position},{validCards},{trickHistory=},{card}')
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
                uHand = getCardsOfRank(validCards, 'U')
                trumplist = createTrumpsList((2, 0))
                oppositionU = set(trumplist) - set(playedU) - set(uHand)
                if len(oppositionU) != 0 and len(uHand) > 0:
                    card = min(uHand)
                else:
                    # we have trump control or no trump
                    # playhighest Rank
                    validNoU = [x for x in validCards if x.rank != 'U']
                    if validNoU:
                        card = min(validCards, key=byRank)
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
                    winningIndex = getTrickWinnerIndex(testTrickHistory, (2, 0))
                    if winningIndex == trickPosIndex:
                        winningCards.append((c, sumTrickHistory(testTrickHistory)))
                if winningCards:
                    # choose card that max scores
                    card = max(winningCards, key=lambda x: x[1])[0]
                    if card.rank == 'U':
                        card = max(getCardsOfRank(validCards, 'U'))
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
                            card = random.choice(validNoUT)
                        else:
                            card = random.choice(validCards)
            # No Lead
            else:
                # Who owns the trick
                trickpos = len(trickHistory)
                # bidwinner already played
                if ringTest(trickLead, trickpos, bidWinnerTablePos):
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
                    # opposition owns trick -> maximise points if U
                    else:
                        # see which cards maximises current score
                        scoringCards = []
                        for c in validCards:
                            testTrickHistory = copy(trickHistory)
                            testTrickHistory.append(c)
                            scoringCards.append((c, sumTrickHistory(testTrickHistory)))
                        card = max(scoringCards, key=lambda x: x[1])[0]
                # bidwinner still to play
                else:
                    # Play Ace if possible, if played -> points
                    playedSuit = trickHistory[0].suit
                    # test if Ace of suit is played
                    if cardInHand(trickHistory, playedSuit, 'A'):
                        scoringCards = []
                        for c in validCards:
                            testTrickHistory = copy(trickHistory)
                            testTrickHistory.append(c)
                            scoringCards.append((c, sumTrickHistory(testTrickHistory)))
                        card = max(scoringCards, key=lambda x: x[1])[0]
                    elif cardInHand(validCards, playedSuit, 'A'):
                        card = getCardOfSuitRank(validCards, playedSuit, 'A')
                    else:
                        card = min(validCards, key=lambda x: x.value)
        if card not in validCards:
            print(f'ERROR{card=},{validCards=}')
            return random.choice(validCards)
        else:
            #print(validCards, card)
            return card
