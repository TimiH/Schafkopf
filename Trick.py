from Card import Card
from CardValues import CardValues
from helper import createTrumps

class Trick:
    def __init__(self, number,leadingPlayer,state):
        self.leadingPlayer = leadingPlayer
        self.gamestate = state
        self.gameMode = gamestate.gameMode
        history = []
        score = 0
        winningPlayer = None

    #Sets the index of the winning card in the History
    def determineWinner(self):
        trumps = createTrumps(self.gameMode)
        trumpsPlayed = [card for card in history if card in trumps]
        if trumpsPlayed:
            winningTrumpIndex = min([trumpsPlayed.index(card) for card in trumpsPlayed])
            winningCard = history[trumpsPlayed[winningTrumpIndex]]
            self.winningPlayer =  history.index(winningCard)
        else:
            firstSuit = self.history[0].suit
            winningRankIndex = min([RANKS.index(card.rank) for card in history if card.suit == firstSuit])
            winninnIndex = history.index(Card(firstSuit,RANKS[winningRankIndex]))
            self.winningPlayer = winninnIndexs

    def sumScore(self):
        score = 0
        for card in history:
            score += card.value
        self.score  = score

    def addCard(self,card):
        self.history.append(card)
