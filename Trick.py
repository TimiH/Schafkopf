from Card import Card
from CardValues import RANKS, VALUES, SUITS, REVERSEDSUITS
from helper import createTrumpsList
from PlayerModels.staticBidding import getCardsOfSuit, cardInHand, trumpsInHandByGamemode
from copy import deepcopy


class Trick:
    def __init__(self, gameDict, leadingPlayer):
        self.leadingPlayer = leadingPlayer
        self.gameDict = gameDict
        self.gameMode = self.gameDict['gameMode']
        self.players = self.gameDict['players']
        self.history = []
        self.score = 0
        self.winningPlayer = None

    #TODO still needed?
    def updatePlayers(self, players):
        self.players = players

    def appendCard(self, card):
        self.history.append(card)
        if self.gameDict['gameMode'][0] == 1:
            suit = self.gameDict['gameMode'][1]
            searchedSuit = REVERSEDSUITS[suit]
            startCard = self.history[0]
            if len(self.history) == 4 and not self.gameDict['ranAway'] and not self.gameDict['searched']:
                if startCard not in self.gameDict['trumpcards'] and self.history[
                    0].suit == searchedSuit and not cardInHand(self.history, searchedSuit, 'A'):
                    self.gameDict['ranAway'] = True
            if card.rank == 'A' and card.suit == reversed[suit]:
                self.gameDict['searched'] = True

    def getValidActionsForHand(self, playerHand):
        if len(playerHand) == 1:
            return playerHand
        if self.gameMode[0] > 1:
            validActions = self.getValidActionsWenzSolo(playerHand)
            return validActions
        else:
            # searched Player?
            suitSearched = REVERSEDSUITS[self.gameMode[1]]
            ace = Card(suitSearched, 'A')
            trumps = self.gameDict['trumpCards']
            # Partner
            if ace in playerHand:
                # Lead
                if len(self.history) == 0:
                    # once Searche/runawayPosssable player can play whatever
                    if self.gameDict['runAwayPossible'] or self.gameDict['ranAway']:
                        return playerHand
                    # while not searched cannot search yourself
                    if not self.gameDict['ranAway']:
                        searchCardsNotA = set(getCardsOfSuit(playerHand, suitSearched, ['O', 'U', 'A']))
                        validCards = set(playerHand) - searchCardsNotA
                        return list(validCards)
                # No Lead
                else:
                    card0 = self.history[0]
                    # play if searched
                    if card0 not in trumps and card0.suit == suitSearched:
                        return [ace]
                    validcards = []
                    # trump played
                    if card0 in trumps:
                        trumpInHand = trumpsInHandByGamemode(playerHand, self.gameMode)
                        if trumpInHand:
                            return trumpInHand
                        else:
                            validcards = playerHand
                    # no trump played
                    else:
                        cardsOfSuit = getCardsOfSuit(playerHand, card0.suit, ['U', 'O'])
                        if cardsOfSuit:
                            return cardsOfSuit
                        else:
                            validcards = playerHand

                    # test if player can play Ace
                    if ace in validcards:
                        if not self.gameDict['ranAway'] or not self.gameDict['searched']:
                            validcards.remove(ace)
                    return validcards

            # Other Players
            else:
                # Lead
                if len(self.history) == 0:
                    return playerHand
                else:
                    card0 = self.history[0]
                    if card0 in trumps:
                        trumpInHand = trumpsInHandByGamemode(playerHand, self.gameMode)
                        if trumpInHand:
                            return trumpInHand
                        else:
                            return playerHand
                    else:
                        cardsOfSuit = getCardsOfSuit(playerHand, card0.suit, ['U', 'O'])
                        if cardsOfSuit:
                            return cardsOfSuit
                        else:
                            return playerHand

    def getValidActionsWenzSolo(self, playerHand):
        if len(self.history) == 0:
            return playerHand
        else:
            card0 = self.history[0]
            trumps = self.gameDict['trumpCards']
            if card0 in trumps:
                trumpInHand = trumpsInHandByGamemode(playerHand, self.gameMode)
                if trumpInHand:
                    return trumpInHand
                else:
                    return playerHand
            else:
                if self.gameMode[0] == 2:
                    cardsOfSuit = getCardsOfSuit(playerHand, card0.suit, ['U'])
                else:
                    cardsOfSuit = getCardsOfSuit(playerHand, card0.suit, ['U', 'O'])
                if cardsOfSuit:
                    return cardsOfSuit
                else:
                    return playerHand

    def getNextValidAction(self):
        currentPlayerIndex = (len(self.history) + self.leadingPlayer) % 4
        playerHand = deepcopy(self.gameDict['playersHands'][currentPlayerIndex])
        validCards = self.getValidActionsForHand(playerHand)
        return validCards, currentPlayerIndex, playerHand, self.history, self.gameState

    def getCurrentPlayerIndex(self):
        currentPlayerIndex = (len(self.history) + self.leadingPlayer) % 4
        return currentPlayerIndex

    def nextAction(self):
        currentPlayerIndex = (len(self.history) + self.leadingPlayer) % 4
        playerHand = deepcopy(self.gameDict['playersHands'][currentPlayerIndex])
        validCards = self.getValidActionsForHand(playerHand)
        self.players[currentPlayerIndex].setHand(playerHand)
        playedCard = self.players[currentPlayerIndex].playCard(validCards, self.gameDict, self.history)
        self.history.append(playedCard)

    def playTrick(self):
        while not self.isFinished():
            self.nextAction()
        self.sumScore()
        self.determineWinner()

    # Sets the index of the winning card in the History
    def determineWinner(self):
        trumps = createTrumpsList(self.gameMode)
        # trumpsPlayed = [card for card in self.history if card in trumps] #TODO use sets here
        trumpsPlayed = list(set(self.history) & set(trumps))
        if trumpsPlayed:
            winningTrumpIndex = min([trumps.index(card) for card in trumpsPlayed])
            winningCard = trumps[winningTrumpIndex]
            winningCardIndex = self.history.index(winningCard)
            winningIndex = (winningCardIndex + self.leadingPlayer) % 4
            self.winningPlayer = winningIndex
        else:
            firstSuit = self.history[0].suit
            winningRankIndex = min([RANKS.index(card.rank) for card in self.history if card.suit == firstSuit])
            winningCardIndex = self.history.index(Card(firstSuit, RANKS[winningRankIndex]))
            winningIndex = (winningCardIndex + self.leadingPlayer) % 4
            self.winningPlayer = winningIndex

    def sumScore(self):
        score = 0
        for card in self.history:
            score += card.value
        self.score = score

    def isFinished(self):
        if len(self.history) == 4:
            return True
        else:
            return False

    # returns all suits from hand without trumps. If empty return hand
    def getSuitsInHand(self, suit, hand):
        trumps = set(createTrumpsList(self.gameMode))
        cards = list([x for x in hand if x.suit == suit and x not in trumps])
        if not cards:
            return hand
        else:
            return cards

    # Adapted from Taschee Github https://github.com/Taschee/schafkopf/blob/master/schafkopf/trick_game.py
    def getValidActionsForHandOld(self, playerHand):
        history = self.history
        hand = set(playerHand)
        trumps = set(createTrumpsList(self.gameMode))
        # hack because Wenz (2,NONE) returns key error #TODO
        if self.gameMode[0] != 2:
            searchedSuit = REVERSEDSUITS[self.gameMode[1]]
        possibleActions = []

        # Speed up for last Trick
        if len(hand) == 1:
            return list(hand)

        # Player has Lead
        if not self.history:
            #Lead and player is partner
            if self.gameMode[0] == 1 and Card(searchedSuit, 'A') in hand:
                if self.gameDict['runAwayPossible'] or self.gameDict['searched']:
                    possibleActions = list(hand)
                else:
                    # Partner may not search himself, but lead the A
                    notPlayable = getCardsOfSuit(list(hand), searchedSuit, ['U', 'O', 'A'])
                    possibleActions = list(hand - set(notPlayable))
            # Lead and not partner
            else:
                possibleActions = list(hand)

        # Player does not have the lead
        else:
            card = self.history[0]
            # Card is Trump
            if card in trumps:
                possibleActions = hand & trumps
                if not possibleActions:
                    possibleActions = list(hand)
                else:
                    possibleActions = list(possibleActions)
            # Card is not Trump
            elif self.gameMode[0] == 1 and Card(searchedSuit, 'A') in hand and card.suit == searchedSuit:
                if not self.gameDict['ranAway']:
                    possibleActions = [Card(searchedSuit, 'A')]
                else:
                    possibleActions = self.getSuitsInHand(card.suit, list(hand))
            else:
                possibleActions = self.getSuitsInHand(card.suit, list(hand))

        if self.gameMode[0] == 1 and Card(searchedSuit, 'A') in possibleActions:
            if not self.gameDict['ranAway'] and len(possibleActions) > 1:
                possibleActions.remove(Card(searchedSuit, 'A'))
        return list(possibleActions)

    def copy(self):
        trick = Trick(self.gameDict, self.leadingPlayer)
        return trick

    # OpenAI stuff
    def addCard(self, card):
        self.history.append(card)
