from Card import Card
from CardValues import RANKS,VALUES,SUITS
from helper import createTrumps, createTrumpsList
from copy import deepcopy,copy

class Trick:
    def __init__(self, number,leadingPlayer,gameCopy):
        self.leadingPlayer = leadingPlayer
        self.gamestate = gameCopy
        self.gameMode = gameCopy.gameMode
        self.players = gameCopy.players
        self.history = []
        self.score = 0
        self.winningPlayer = None

    def nextAction(self):
        print(self.history)
        currentPlayerIndex = (len(self.history) + self.leadingPlayer) % 4
        validCards = self.getValidActionsForPlayerNew(self.players[currentPlayerIndex])
        playedCard = self.players[currentPlayerIndex].playCard(validCards,self.gamestate)
        self.history.append(playedCard)

    def playTrick(self):
        actionsMissing = 4 - len(self.history)
        for n in range(actionsMissing):
            self.nextAction()
        self.sumScore()


    def getValidActionsForPlayer(self,player):
        possibleActions = copy(player.hand)
        trumps = createTrumps(self.gameMode)
        reversed = dict(zip(SUITS.values(),SUITS.keys()))

        #Check if game is SOLO
        if self.gameMode[0] != 1:
            #LeadingPlayer has full actionspace
            if not self.history:
                return possibleActions
            #Check if trumps is first Card
            else:
                card = self.history[0]
                if card in trumps:
                    #remainingActions = list(filter(lambda x: x in trumps,possibleActions))
                    possibleActions = set(possibleActions)
                    remainingActions = possibleActions&trumps
                    if not remainingActions:
                        return list(possibleActions)
                    else:
                        return list(remainingActions)
                #No trump as first Card
                else:
                    suit = card.suit
                    remainingActions = list(filter(lambda x: x.suit == suit and x not in trumps,possibleActions))
                    if not remainingActions:
                        return possibleActions
                    else:
                        return remainingActions
        #PartnerGame
        else:
            suit = reversed[self.gameMode[1]]
            #See if player is Partner in Team with Ace
            if self.players.index(player) == self.gamestate.offensivePlayers[1]:
                #Player has the Lead
                if not self.history:
                    #RunningAway True return all
                    if self.gamestate.runAwayPossible:
                        return possibleActions
                    #RunningAway False
                    else:
                        #Once it has been searched return All
                        if self.gamestate.searched:
                            return possibleActions
                        #If not Player can play all cards but the colour thats being searched for
                        else:
                            remainingActions = list(filter(lambda x: x.rank not in ['U','O'] and x.suit != suit,possibleActions))
                            return remainingActions
                #Play does not have the lead
                else:
                    card = self.history[0]
                    if self.gamestate.searched:
                        if card in trumps:
                            possibleActions = set(possibleActions)
                            remainingActions = possibleActions&trumps
                            #Does not have Trump
                            if not remainingActions:
                                possibleActions = list(possibleActions)
                                if len(possibleActions) > 1:
                                    searchedSuit = reversed[self.gameMode[1]]
                                    possibleActions = possibleActions.remove(Card(searchedSuit,'A'))
                                return possibleActions
                            else:
                                return list(remainingActions)

                        #First card is no trump
                        else:
                            suit = card.suit
                            remainingActions = list(filter(lambda x: x.suit == suit and x not in trumps,possibleActions))
                            if not remainingActions:
                                return possibleActions
                            else:
                                return remainingActions
                    #Game has not been searched
                    else:
                        if card in trumps:
                            possibleActions = set(possibleActions)
                            remainingActions = possibleActions&trumps
                            if not remainingActions:
                                possibleActions = list(possibleActions)
                                if len(possibleActions) > 1:
                                    searchedSuit = reversed[self.gameMode[1]]
                                    possibleActions = possibleActions.remove(Card(searchedSuit,'A'))
                                return possibleActions
                            #Does not have trump but cant play Ace
                            else:
                                if len(possibleActions) > 1:
                                    searchedSuit = reversed[self.gameMode[1]]
                                    possibleActions = possibleActions.remove(Card(searchedSuit,'A'))
                                return possibleActions
                        #card is not it trump
                        else:
                            suit = card.suit
                            searchedSuit = reversed[self.gameMode[1]]
                            #check if Ace is being Searched
                            if searchedSuit == suit:
                                return [Card(searchedSuit,'A')]
                            remainingActions = list(filter(lambda x: x.suit == suit and x not in trumps,possibleActions))
                            if not remainingActions:
                                #Ace cannot be played until last trick
                                if len(possibleActions) > 1:
                                    possibleActions = possibleActions.remove(Card(searchedSuit,'A'))
                                return possibleActions
                            else:
                                return remainingActions
            #Player is not Partner with Ace
            else:
                #LeadingPlayer has full actionspace
                if not self.history:
                    return possibleActions
                #Check if trumps is first Card
                card = self.history[0]
                if card in trumps:
                    remainingActions = list(filter(lambda x: x in trumps,possibleActions))
                    #Does not have Trump
                    if not remainingActions:
                        return possibleActions
                    else:
                        return remainingActions
                #No trump as first Card
                else:
                    suit = card.suit
                    remainingActions = list(filter(lambda x: x.suit == suit and x not in trumps,possibleActions))
                    if not remainingActions:
                        return possibleActions
                    else:
                        return remainingActions

    #Sets the index of the winning card in the History
    def determineWinner(self):
        trumps = createTrumpsList(self.gameMode)
        trumpsPlayed = [card for card in self.history if card in trumps]
        if trumpsPlayed:
            winningTrumpIndex = min([trumpsPlayed.index(card) for card in trumpsPlayed])
            winningCard = trumpsPlayed[winningTrumpIndex]
            self.winningPlayer =  self.history.index(winningCard)
        else:
            firstSuit = self.history[0].suit
            winningRankIndex = min([RANKS.index(card.rank) for card in self.history if card.suit == firstSuit])
            winninnIndex = self.history.index(Card(firstSuit,RANKS[winningRankIndex]))
            self.winningPlayer = winninnIndex

    def sumScore(self):
        score = 0
        for card in self.history:
            score += card.value
        self.score  = score

    #returns all suits from hand without trumps. If empty return hand
    def getSuitsInHand(self,suit,hand):
        trumps = createTrumps(self.gameMode)
        cards = list(filter(lambda x: x.suit == suit and x not in trumps,hand))
        if not cards:
            return hand
        else:
            return cards

    #Adapted from Taschee Github
    def getValidActionsForPlayerNew(self, player):
        hand = set(copy(player.hand))
        trumps = createTrumps(self.gameMode)
        reversed = dict(zip(SUITS.values(),SUITS.keys()))
        searchedSuit = reversed[self.gameMode[1]]
        print("Search suit:",searchedSuit)
        possibleActions = []
        #Player has Lead
        if not self.history:
            if self.gameMode[0] == 1 and self.players.index(player) == self.gamestate.offensivePlayers[1]:
                if self.gamestate.runAwayPossible:
                    possibleActions = list(hand)
                else:
                    possibleActions = list(hand)
                    possibleActions.remove(Card(searchedSuit,'A'))
            else:
                possibleActions = list(hand)

        #Player does not have the lead
        else:
            card = self.history[0]
            #Card is Trump
            if card in trumps:
                possibleActions = hand & trumps
                if not possibleActions:
                    possibleActions = list(hand)
                else:
                    print("not Lead and possibleActions not empty")
                    print(possibleActions)
                    possibleActions = list(possibleActions)
            #Card is not Trump
            elif self.gameMode[0] == 1 and self.players.index(player) == self.gamestate.offensivePlayers[1] and card.suit == searchedSuit:
                if not self.gamestate.ranAway:
                    possibleActions = [Card(searchedSuit,'A')]
                else:
                    possibleActions = self.getSuitsInHand(card.suit, list(hand))
            else:
                possibleActions = self.getSuitsInHand(card.suit, list(hand))


        if self.gameMode[0] == 1 and Card(searchedSuit,'A') in possibleActions:
            if not self.gamestate.ranAway and len(possibleActions) > 1:
                    possibleActions.remove(Card(searchedSuit,'A'))

        return possibleActions
