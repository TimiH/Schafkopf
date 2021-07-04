import random

from Player import Player
from PlayerModels.staticBidding import choseSoloGame, choseWenzGameRevised, choseTeamGame, choseWenzGame
from PlayerModels.staticBidding import getCardsOfRank, cardInHand, rankInHand, getCardOfSuitRank, \
    trumpsInHandByGamemode, getCardsOfSuit
from helper import createTrumpsList, byRank, getTrickWinnerIndex, sumTrickHistory, ringTest, sortTrump, getParnterPos, \
    getValidWinners
from CardValues import SUITS, REVERSEDSUITS
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
        # if max != (0, 0):
        #     print((max, self.hand))
        return max

    def playCard(self, validCards, gameDict, trickHistory):
        if len(validCards) == 1:
            # print(f'Only:{self.position},{self.hand=},{validCards},{trickHistory=},{validCards[0]}')
            return validCards[0]
        mode, _ = gameDict['gameMode']
        card = None
        if mode == 1:
            card = self.playTeamCard(validCards, gameDict, trickHistory)
        if mode == 2:
            card = self.playWenzCard(validCards, gameDict, trickHistory)
        if mode == 3:
            card = self.playSoloCard(validCards, gameDict, trickHistory)
        #print(f'{self.position},{self.hand=},{validCards},{trickHistory=},{card}')
        return card

    def playTeamCard(self, validCards, gameDict, trickHistory):
        offensivePlayers = gameDict['offensivePlayers']
        # Decide which Role
        card = None
        if self.position == offensivePlayers[0]:
            card = self.playTeamBidWinner(validCards, gameDict, trickHistory)
        elif self.position == offensivePlayers[1]:
            card = self.playTeamPartner(validCards, gameDict, trickHistory)
        else:
            card = self.playTeamOpposition(validCards, gameDict, trickHistory)
        if not card:
            raise Exception
        else:
            return card

    def playTeamBidWinner(self, validCards, gameDict, trickHistory):
        card = None
        gameMode = gameDict['gameMode']
        searchedSuit = REVERSEDSUITS[gameMode[1]]
        trumps = createTrumpsList(gameMode)
        # Lead
        if len(trickHistory) == 0:
            # play highest trump
            trumpsInHand = trumpsInHandByGamemode(validCards, gameMode)
            if trumpsInHand:
                orderedTrump = sortTrump(trumpsInHand)
                card = orderedTrump[0]
            else:
                # Play aces or high color
                validCardsNoSearch = set(validCards) - set(getCardsOfSuit(validCards, ['O', 'U']))
                if validCardsNoSearch:
                    card = max(validCardsNoSearch, key=byRank)
                else:
                    card = random.choice(validCards)
        # No Lead
        else:
            trickpos = len(trickHistory)
            currentWinnerTrickPos = getTrickWinnerIndex(trickHistory, (2, 0))
            winningTableIndex = (currentWinnerTrickPos + gameDict['leadingPlayer']) % 4
            # partner known?
            if gameDict['searched'] or gameDict['ranAway']:
                partnerPos = getParnterPos(self.position, gameDict['offensivePlayers'])
                # Parnter owns trick
                if winningTableIndex == partnerPos:
                    card = max(validCards, key=lambda x: x.value)
                # Opposition owns trick
                else:
                    winningCards = getValidWinners(trickHistory, validCards, gameMode)
                    if winningCards:
                        card = max(winningCards, key=lambda x: x[1])[0]
                    else:
                        validNoTrump = list(set(validCards) - set(trumps))
                        if validNoTrump:
                            card = min(validNoTrump, key=lambda x: x.value)
                        else:
                            card = min(validCards, key=lambda x: x.value)
            # partner not known
            else:
                # greedy or min
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

    def playTeamPartner(self, validCards, gameDict, trickHistory):
        card = None
        partnerPos = getParnterPos(self.position, gameDict['offensivePlayers'])
        gameMode = gameDict['gameMode']
        searchedSuit = REVERSEDSUITS[gameMode[1]]
        trumps = gameDict['trumpCards']

        # Lead
        if len(trickHistory) == 0:
            # if runaway possible run away
            if not gameDict['searched'] and not gameDict['ranAway'] and gameDict['runAwayPossible']:
                runawayCards = getCardsOfSuit(validCards, searchedSuit, ['O', 'U'])
                card = min(runawayCards, key=lambda x: x.value)
            else:
                # play Trump
                trumpsInHand = trumpsInHandByGamemode(validCards, gameMode)
                if trumpsInHand:
                    orderedTrump = sortTrump(trumpsInHand)
                    card = orderedTrump[0]
                else:
                    # try play cards not searched suit
                    validCardsNoSearch = list(set(validCards) - set(getCardsOfSuit(validCards, ['O', 'U'])))
                    if validCardsNoSearch:
                        card = max(validCardsNoSearch, key=byRank)
                    else:
                        card = random.choice(validCards)
        # No Lead
        else:
            # Does bidWinner own the trick?
            currentWinnerTrickPos = getTrickWinnerIndex(trickHistory, gameMode)
            winningTableIndex = (currentWinnerTrickPos + gameDict['leadingPlayer']) % 4
            if winningTableIndex == partnerPos:
                card = max(validCards, key=lambda x: x.value)
            else:
                # can we trick?
                winningCards = getValidWinners(trickHistory, validCards, gameMode)
                if winningCards:
                    card = max(winningCards, key=lambda x: x[1])[0]
                else:
                    card = min(validCards, key=lambda x: x.value)
        if not card:
            raise Exception
        return card

    def playTeamOpposition(self, validCards, gameDict, trickHistory):
        card = None
        partnerPos = getParnterPos(self.position, gameDict['offensivePlayers'])
        gameMode = gameDict['gameMode']
        searchedSuit = REVERSEDSUITS[gameMode[1]]
        trumps = gameDict['trumpCards']
        # lead
        if len(trickHistory) == 0:
            # Can we search?
            if not gameDict['searched'] and not gameDict['ranAway']:
                searchCards = getCardsOfSuit(validCards, searchedSuit, ['U', 'O'])
                if searchCards:
                    card = random.choice(searchCards)
                    return card
            # Play Aces & no naked T
            validNoTrump = list(set(validCards) - set(trumps))
            aces = getCardsOfRank(validNoTrump, 'A')
            if aces:
                card = random.choice(aces)
            else:
                validNoUT = [x for x in validNoTrump if x.rank != 'T']
                if validNoUT:
                    card = random.choice(validNoUT)
                else:
                    card = random.choice(validCards)
        # No Lead
        else:
            trickpos = len(trickHistory)
            currentWinnerTrickPos = getTrickWinnerIndex(trickHistory, (2, 0))
            winningTableIndex = (currentWinnerTrickPos + gameDict['leadingPlayer']) % 4
            # Partner known?
            if gameDict['searched'] or gameDict['ranAway']:
                partnerPos = getParnterPos(self.position, gameDict['offensivePlayers'])
                # Who owns the trick?
                if winningTableIndex == partnerPos:
                    # opposition owns the trick -> max score
                    card = max(validCards, key=lambda x: x.value)
                else:
                    # bidWinners own the trick
                    winningCards = getValidWinners(trickHistory, validCards, gameMode)
                    if winningCards:
                        card = max(winningCards, key=lambda x: x[1])[0]
                    else:
                        validNoTrump = list(set(validCards) - set(trumps))
                        if validNoTrump:
                            card = min(validNoTrump, key=lambda x: x.value)
                        else:
                            card = min(validCards, key=lambda x: x.value)
            # Partner unknown
            else:
                # Partner unknown: greedy or lowest
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

    def playSoloCard(self, validCards, gameDict, trickHistory):
        card = None
        gameMode = gameDict['gameMode']
        trumps = gameDict['trumpCards']
        trumpInHand = trumpsInHandByGamemode(validCards, gameMode)
        # Decide Player or Opposition
        if self.position == gameDict['offensivePlayers'][0]:
            # Lead
            if len(trickHistory) == 0:
                playedTrump = trumpsInHandByGamemode(gameDict['cardsPlayed'], gameMode)
                oppositionU = set(trumps) - set(playedTrump) - set(trumpInHand)
                # while opposition has trump play trump
                if len(oppositionU) != 0 and len(trumpInHand) > 0:
                    orderedTrump = sortTrump(trumpInHand)
                    card = orderedTrump[0]
                else:
                    # we have trump control or no trump
                    validCardsNoTrump = list(set(validCards) - set(trumpInHand))
                    if validCardsNoTrump:
                        card = max(validCardsNoTrump, key=byRank)
                    else:
                        card = random.choice(validCards)
            # noLead
            else:
                # can we trick
                winningCards = getValidWinners(trickHistory, validCards, gameMode)
                # we can trick
                if winningCards:
                    # choose card that max scores
                    card = max(winningCards, key=lambda x: x[1])[0]
                    # chose lowest suit O
                    if card.rank == 'O':
                        card = max(getCardsOfRank(validCards, 'O'))
                else:
                    card = min(validCards, key=lambda x: x.value)
        # Opposition
        else:
            # Lead
            bidWinnerTablePos = gameDict['offensivePlayers'][0]
            trickLead = gameDict['leadingPlayer']
            if len(trickHistory) == 0:
                # avoid Trump
                validNoTrump = list(set(validCards) - set(trumpInHand))
                if not validNoTrump:
                    card = random.choice(validCards)
                # play Aces if possible
                aces = getCardsOfRank(validNoTrump, 'A')
                if aces:
                    card = random.choice(aces)
                else:
                    validNoTrumpNoT = [x for x in validNoTrump if x.rank != 'T']
                    if validNoTrumpNoT:
                        card = random.choice(validNoTrumpNoT)
                    else:
                        card = random.choice(validCards)
            # no Lead
            else:
                trickpos = len(trickHistory)
                # bidwinner already played
                if ringTest(trickLead, trickpos, bidWinnerTablePos):
                    currentWinnerTrickPos = getTrickWinnerIndex(trickHistory, gameMode)
                    winningTableIndex = (currentWinnerTrickPos + trickLead) % 4
                    # bidwinner currently winning
                    if bidWinnerTablePos == winningTableIndex:
                        # test cards if winning and append (card,trickscore)
                        winningCards = getValidWinners(trickHistory, validCards, gameMode)
                        if winningCards:
                            card = max(winningCards, key=lambda x: x[1])[0]
                        # cant win
                        else:
                            if trickHistory[0] in trumps and trumpInHand:
                                card = sortTrump(trumpInHand)[-1]
                            else:
                                validNoTrump = list(set(validCards) - set(trumpInHand))
                                if validNoTrump:
                                    card = min(validNoTrump, key=lambda x: x.value)
                                else:
                                    card = random.choice(validCards)
                    # opposition winning
                    else:
                        scoringCards = []
                        for c in validCards:
                            testTrickHistory = copy(trickHistory)
                            testTrickHistory.append(c)
                            scoringCards.append((c, sumTrickHistory(testTrickHistory)))
                        card = max(scoringCards, key=lambda x: x[1])[0]
                # bidwinner yet to play
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
        if not card:
            raise Exception
        else:
            return card

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
                    card = random.choice(validCards)
            # noLead
            else:
                trickPos = len(trickHistory)
                # can we trick
                # (card, trickscore)
                winningCards = getValidWinners(trickHistory, validCards, (2, 0))
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
                        winningCards = getValidWinners(trickHistory, validCards, (2, 0))
                        if winningCards:
                            card = max(winningCards, key=lambda x: x[1])[0]
                        else:
                            # choose lowest card by value not U
                            validNoU = [x for x in validCards if x.rank != 'U']
                            if validNoU:
                                card = min(validNoU, key=lambda x: x.value)
                            else:
                                card = min(validCards, key=lambda x: x.value)
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
        if not card:
            raise Exception
        else:
            return card

    def getValidWinners(trickHistory, validCards, gameMode):
        trickPos = len(trickHistory)
        winningCards = []
        for c in validCards:
            testTrickHistory = copy(trickHistory)
            testTrickHistory.append(c)
            winningIndex = getTrickWinnerIndex(testTrickHistory, gameMode)
            if winningIndex == trickPos:
                winningCards.append((c, sumTrickHistory(testTrickHistory)))
