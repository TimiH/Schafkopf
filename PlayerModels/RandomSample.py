from helper import createTrumps
from CardValues import RANKS, SUITS
from operator import itemgetter
from PlayerModels.RandomPlayer import RandomPlayer
from Player import Player
from PlayerModels.SampleMaster import SampleMaster
from helper import sortHand
import random
__metaclass__ = type

class RandomSample(Player):
    def __init__(self,name):
        self.name = name
        self.hand = []

    def setHand(self,cards):
        self.hand = sortHand(cards)

    def playCard(self,validCards,gamestate,trickHistory):
        #If no cards or 1 card
        if len(validCards) == 0:
            print("noValidCards")
        if len(validCards) == 1:
            return validCards[0]
        else:
            position = self.getPosition(gamestate)
            print("--------------------------------")
            print("SampleMaster Position",position)
            masternode = SampleMaster(gamestate,validCards,self.hand,position)
            scoreArray = []
            for child in masternode.children:
                print("TreeNode:",child.card,child.rewards,masternode.playerPosition)
                scoreArray.append(child.rewards[position])
            best = max(scoreArray)
            bestIndex = scoreArray.index(best)
            card = masternode.children[bestIndex].card
            #print("Hand:{},Playing: {},validCards: {}".format(self.hand,card,validCards))
            #self.hand.remove(card)
            return card

    #Somewhat adopted from https://github.com/Taschee/schafkopf/blob/master/schafkopf/players/heuristics_player.py
    def makeBid(self,validBids):
        teamGameChoice = self.choseTeamGame(validBids)
        wenzGameChoice = self.choseWenzGame(validBids)
        soloGameChoice = self.choseSoloGame(validBids)
        bids = []

        max = (None,None)
        if teamGameChoice[0]>max[0]:
            max = teamGameChoice
        if wenzGameChoice[0]>max[0]:
            max = wenzGameChoice
        if soloGameChoice[0]>max[0]:
            max = soloGameChoice
        #print("PLAYERCHOICES",max,teamGameChoice,wenzGameChoice,soloGameChoice)
        if max != (None,None):print(max,self.hand)
        return max

    def sortHand(self,state):
        pass

    def choseTeamGame(self, validBids):
        possibleTeam = list(filter(lambda x: x[0]==1,validBids))
        ret = (None,None)
        if not possibleTeam:
            return (None,None)

        uCount = self.countCardInHand('U')
        oCount = self.countCardInHand('O')
        tcount = self.countColoursInHand('Herz')
        aCount = self.countCardInHand('A')
        countCoulour = self.countColoursInHand()
        total = uCount + oCount+tcount
        #Decide if possible otherwise delete list
        if total >=4 and oCount >= 1 and uCount >=1 and aCount >=2 and any(x.rank == 'O' and x.rank in ['Eichel','Gras','Herz'] for x in self.hand):
            pass
        elif total >=5 and oCount >=2 and uCount >= 1 and all(x > 0 for x in countCoulour):
            pass
        elif total >=5 and (countCoulour[0] == 0 or countCoulour[1] == 0 or countCoulour[3] ==0 ):
            pass
        elif total >=6:
            pass
        else:
            possibleTeam = []

        #Decide which of them is viable
        if possibleTeam:
            first = possibleTeam[0]
            for mode in possibleTeam:
                if countCoulour[mode[1]] < countCoulour[first[1]]:
                    first = mode
            ret = first
        return ret

    def choseSoloGame(self, validBids):
        uCount = self.countCardInHand('U')
        oCount = self.countCardInHand('O')
        chosenSolo = (None, None)
        if (uCount + oCount) <3:
            return chosenSolo
        else:
            #Find the solo with the most trumps or leave it
            max = len(self.trumpsInHandByGamemode((3,0)))
            for solo in validBids:
                if solo[0] == 3:
                    trumpsInHand = self.trumpsInHandByGamemode(solo)
                    if len(trumpsInHand) >=5 and len(trumpsInHand) > max:
                        chosenSolo = solo

        if chosenSolo != (None,None):
            trumpsInHand = self.trumpsInHandByGamemode(chosenSolo)
            if len(trumpsInHand) >= 6:
                return chosenSolo
            elif len(trumpsInHand) == 5:
                reversed = dict(zip(SUITS.values(),SUITS.keys()))
                if self.countSpatzenForTrump(reversed[chosenSolo[1]]) >=2:
                    chosenSolo = (None, None)

        return chosenSolo

    #Possibly look at 2U(top 2),2A
    def choseWenzGame(self, validBids):
        uCount = self.countCardInHand('U')
        aCount = self.countCardInHand('A')
        ret = (None,None)
        if uCount >=3:
            if aCount >=2:
                ret = (2,None)
            elif aCount == 1:
                ace = list(filter(lambda x: x.rank == 'A', self.hand))[0]
                aceSuitsInHand = self.countColoursInHand(ace.suit)
                if aceSuitsInHand >=3:
                    ret = (2,None)
        return ret


    def trumpsInHandByGamemode(self,gameMode):
        trumps = createTrumps(gameMode)
        trumpsInHand =  set(self.hand) & trumps
        return trumpsInHand

    def countCardInHand(self,rank):
        count = 0
        for c in self.hand:
            if c.rank == rank:
                count += 1
        return count

    #Returns either a count for all colours as list [E,G,H,S] or count for specific colour
    def countColoursInHand(self, colour=None):
        counts = [0,0,0,0]
        if colour == None:
            for card in self.hand:
                if card.rank not in ['U','O']:
                    counts[SUITS[card.suit]] +=1
            return counts
        else:
            count=0
            for card in self.hand:
                if card.suit == colour and card.rank not in ['U','O']:
                    count +=1
            return count

    def countSpatzenForTrump(self,suit):
        count = 0
        for card in self.hand:
            if card.rank != 'A' and card.suit != suit:
                count += 1
        return count
