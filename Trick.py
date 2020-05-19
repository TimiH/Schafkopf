from Card import Card
from CardValues import RANKS, VALUES, SUITS
from helper import createTrumps, createTrumpsList
from copy import deepcopy, copy


class Trick:
    def __init__(self, number, leadingPlayer, copy):
        self.leadingPlayer = leadingPlayer
        self.gamestate = None
        self.gameMode = None
        self.players = None
        self.history = []
        self.score = 0
        self.winningPlayer = None

    # Somewhat hacky but necessary to avoid empty references in current trick
    def setMembers(self):
        self.gameMode = self.gamestate.gameMode
        self.players = self.gamestate.players

    def updatePlayers(self, players):
        self.players = players

    def nextAction(self):
        # print(self.history)
        currentPlayerIndex = (len(self.history) + self.leadingPlayer) % 4
        validCards = self.getValidActionsForPlayerNew(self.players[currentPlayerIndex])
        playedCard = self.players[currentPlayerIndex].playCard(validCards, self.gamestate, self.history)
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
        cards = list(filter(lambda x: x.suit == suit and x not in trumps, hand))
        if not cards:
            return hand
        else:
            return cards

    # Adapted from Taschee Github https://github.com/Taschee/schafkopf/blob/master/schafkopf/trick_game.py
    def getValidActionsForPlayerNew(self, player):
        hand = set(copy(player.hand))
        trumps = createTrumps(self.gameMode)
        reversed = dict(zip(SUITS.values(), SUITS.keys()))

        # hack because Wenz (2,NONE) returns key error #TODO
        if self.gameMode[0] != 2:
            searchedSuit = reversed[self.gameMode[1]]
        possibleActions = []

        # Speed up for last Trick
        if len(hand) == 1:
            return list(hand)

        # Player has Lead
        if not self.history:
            if self.gameMode[0] == 1 and Card(searchedSuit, 'A') in hand:
                if self.gamestate.runAwayPossible and self.gamestate.searched:
                    possibleActions = list(hand)
                else:
                    possibleActions = list(hand)
                    possibleActions.remove(Card(searchedSuit, 'A'))
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
                if not self.gamestate.ranAway:
                    possibleActions = [Card(searchedSuit, 'A')]
                else:
                    possibleActions = self.getSuitsInHand(card.suit, list(hand))
            else:
                possibleActions = self.getSuitsInHand(card.suit, list(hand))

        if self.gameMode[0] == 1 and Card(searchedSuit, 'A') in possibleActions:
            if not self.gamestate.ranAway and len(possibleActions) > 1:
                possibleActions.remove(Card(searchedSuit, 'A'))
        return possibleActions
