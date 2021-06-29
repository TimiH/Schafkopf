from Card import Card
from CardValues import RANKS, VALUES, SUITS, REVERSEDSUITS
from helper import createTrumps, createTrumpsList
from PlayerModels.staticBidding import getCardsOfSuit, cardInHand
from copy import deepcopy, copy


class Trick:
    def __init__(self, gameDict, leadingPlayer):
        self.leadingPlayer = leadingPlayer
        self.gameDict = gameDict
        self.gameMode = self.gameDict['gameMode']
        self.players = self.gameDict['players']
        self.history = []
        self.score = 0
        self.winningPlayer = None

    def updatePlayers(self, players):
        self.players = players

    def appendCard(self, card):
        self.history.append(card)
        if self.gameDict['gameMode'][0] == 1:
            suit = self.gameDict['gameMode'][1]
            searchedSuit = REVERSEDSUITS[suit]
            if len(self.history) == 4 and not self.gameDict['ranAway'] and not self.gameDict['searched']:
                if self.history[0].suit == searchedSuit and not cardInHand(self.history, searchedSuit, 'A'):
                    self.gameDict['ranAway'] = True
            if card.rank == 'A' and card.suit == reversed[suit]:
                self.gameDict['searched'] = True

    def getNextValidAction(self):
        currentPlayerIndex = (len(self.history) + self.leadingPlayer) % 4
        playerHand = self.gameDict['playersHands'][currentPlayerIndex]
        validCards = self.getValidActionsForHand(playerHand)
        return validCards, currentPlayerIndex, playerHand, self.history

    def nextAction(self):
        currentPlayerIndex = (len(self.history) + self.leadingPlayer) % 4
        playerHand = self.gameDict['playersHands'][currentPlayerIndex]
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
        trumps = createTrumps(self.gameMode)
        cards = list([x for x in hand if x.suit == suit and x not in trumps])
        if not cards:
            return hand
        else:
            return cards

    # Adapted from Taschee Github https://github.com/Taschee/schafkopf/blob/master/schafkopf/trick_game.py
    def getValidActionsForHand(self, playerHand):
        hand = set(playerHand)
        trumps = createTrumps(self.gameMode)
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
        return possibleActions

    def copy(self):
        trick = Trick(self.gameDict, self.leadingPlayer)
        return trick

    #OpenAI stuff
    def addCard(self,card):
        self.history.append(card)

