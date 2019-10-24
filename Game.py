from Card import Card
from Deck import Deck
from Bidding import Bidding
import random
from copy import deepcopy
from Player import Player
from CardValues import SUITS, RANKS, VALUES
from helper import canRunaway,createTrumpsList
from Trick import Trick
from Rewards import REWARDS

class Game:
    def __init__(self, players,leadingPlayer):
        self.players = players #List of players and Positons
        self.scores = [0,0,0,0]
        self.leadingPlayer = leadingPlayer
        self.history = []
        self.cardsPlayed = []

        self.gameMode = None
        self.bids = [(None,None)]
        self.offensivePlayers = [] #Index 0 is the WinningBid, 1 is the other player
        self.runAwayPossible = None

        self.currentTrick = None
        self.ranAway = False
        self.searched = False
        self.laufende = 0

        self.rewards = [0,0,0,0]
        self.trumpCards = ()

    def isFinished(self):
        if len(self.history) == 8:
            return True
        else:
            return False

    def setupGame(self):
        deck = Deck()
        deck.shuffle()

        #Dealing cards
        for p in self.players:
            p.setHand(deck.deal(8))

    def shufflePositon(self):
        random.shuffle(self.players)

    def copy(self):
        return deepcopy(self)

    #Sets the bids, gameModes and offensivePlayers
    def setGameMode(self,bidding):
        self.bids = bidding.getBids()
        self.gameMode = bidding.winningBid
        self.offensivePlayers.append(bidding.winningIndex)

        #finds second offensive player in team mode
        reversed = dict(zip(SUITS.values(),SUITS.keys()))
        if self.gameMode[0] == 1:
            suit = self.gameMode[1]
            for p in self.players:
                for card in p.hand:
                    if card.rank == 'A':
                        if card.suit == reversed[suit]:
                            playerIndex = self.players.index(p)
                            #self.offensivePlayers.append(playerIndex)
                            self.offensivePlayers.append(playerIndex)

    def setRunAwayPossible(self):
        if len(self.offensivePlayers) >1:
            player = self.players[self.offensivePlayers[1]]
            self.runAwayPossible = canRunaway(player,self.gameMode)
        else:
            self.runAwayPossible = False

    def setSearched(self, trick):
        mode, suit = self.gameMode
        if mode != 1:
            return
        else:
            reversed = dict(zip(SUITS.values(),SUITS.keys()))
            ace =  Card(reversed[suit],'A')
            for c in trick.history:
                if c == ace:
                    self.searched = True
                    return

    def removeCards(self,history):
        count = 0
        for player in self.players:
            for c in history:
                if c in player.hand:
                    player.hand.remove(c)
                    count += 1

    #Creates a tuple ((Cards),leadingPlayer,winningPLayer)
    def historyFromTrick(self,trick):
        if not trick.isFinished():
            "UNFINNISHED TRICK"
            return
        cards = tuple(trick.history)
        self.history.append((cards,trick.leadingPlayer,trick.winningPlayer))
        self.cardsPlayed += (trick.history)

    def mainGame(self):
        self.setupGame()
        copy = self.copy()
        bidding = Bidding(copy,self.leadingPlayer)
        bidding.biddingPhase()
        self.setGameMode(bidding)
        self.setRunAwayPossible()
        self.setLaufende()

        if self.gameMode == (None,None):
            print("no game mode")
            return
        # print("Bids:",self.bids,"\nLeadingPlayer:",self.leadingPlayer)
        # print("Gamemode: {},\nOffensive players: {}\n".format(self.gameMode,self.offensivePlayers))
        lead = self.leadingPlayer
        for n in range(8):
            #TODO FIX THIS
            trick = Trick(n,lead,None)
            self.currentTrick = trick
            copy = self.copy()
            trick.gamestate = copy
            trick.setMembers()
            trick.playTrick()
            self.scores[trick.winningPlayer] += trick.score
            lead = trick.winningPlayer
            # self.tricks.append(trick)
            self.removeCards(trick.history)
            self.historyFromTrick(trick)
        self.setRewards()
        # print(self.offensivePlayers)
        # print(self.scores)


    def continueGame(self):
        if not self.currentTrick.isFinished():
            self.currentTrick.playTrick()

        while not self.isFinished():
            trick = Trick(len(self.history)+1,self.currentTrick.winningPlayer,None)
            self.currentTrick = trick
            copy = self.copy()
            trick.gamestate = copy
            trick.setMembers()
            trick.playTrick()
            self.scores[trick.winningPlayer] += trick.score
            lead = trick.winningPlayer
            self.removeCards(trick.history)
            self.historyFromTrick(trick)

    def offenceWon(self):
        if not self.isFinished:
            print("Game not Finished")
        scoreOffense = 0
        for p in self.offensivePlayers:
            scoreOffense += self.scores[p]

        if scoreOffense > 61:
            return True
        else:
            return False

    def setLaufende(self):
        if self.gameMode == None:
            print("No Bid in gamestate")

        trumps = createTrumpsList(self.gameMode)
        offensive = set()
        defensive = set()

        #create combined set trupms for both teams
        for p in self.offensivePlayers:
            offensive = offensive | set(self.players[p].hand)
        offensive = set(trumps) & offensive
        defensive = set(trumps) - offensive
        countOffense = 0
        for card in trumps:
            if card in offensive:
                countOffense += 1
            else:
                break

        countDefense = 0
        for card in trumps:
            if card in defensive:
                countDefense += 1
            else:
                break

        if self.gameMode[0] == 2:
            if countDefense >= 2 or countOffense >= 2:
                self.laufende = max([countDefense,countDefense])
        else:
            if countDefense >= 3 or countOffense >= 3:
                self.laufende = max([countDefense,countDefense])

    def setRewards(self):
        schneider = False
        schwarz = False
        scoreOffense = 0
        for p in self.offensivePlayers:
            scoreOffense += self.scores[p]
        #check for Draw
        if scoreOffense == 60:
            self.rewards = [0,0,0,0]
            return
        #Check if schneider
        elif scoreOffense > 90 or scoreOffense < 31:
            schneider = True
        #Check if one team scored all tricks
        trickCount = 0
        for t in self.history:
            if t[2] in self.offensivePlayers:
                trickCount += 1
        if trickCount == 8 or trickCount == 0:
            schwarz = True
        if self.gameMode[0] == 1:
            baseReward = REWARDS['TEAM']
        elif self.gameMode[0] == 2:
            baseReward = REWARDS['WENZ']
        elif self.gameMode[0] == 3:
            baseReward = REWARDS['SOLO']

        reward = baseReward + REWARDS['LAUFENDE']*self.laufende + REWARDS['SCHNEIDER']*schneider + REWARDS['SCHWARZ']*schwarz

        if self.gameMode[0] == 1:
            for s in range(0,4):
                if self.offenceWon():
                    if s in self.offensivePlayers:
                        self.rewards[s] = reward
                    else:
                        self.rewards[s] = -1*reward
                else:
                    if s in self.offensivePlayers:
                        self.rewards[s] = -1*reward
                    else:
                        self.rewards[s] = reward
        else:
            for s in range(0,4):
                if self.offenceWon():
                    if s in self.offensivePlayers:
                        self.rewards[s] = 3*reward
                    else:
                        self.rewards[s] = -1*reward
                else:
                    if s in self.offensivePlayers:
                        self.rewards[s] = -3*reward
                    else:
                        self.rewards[s] = 1*reward
