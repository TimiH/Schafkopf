from CardValues import SUITS
from GameModes import MODES
from operator import itemgetter
from Card import Card
from copy import deepcopy,copy

class Bidding:
    def __init__(self, gameCopy):
        self.gameCopy = gameCopy
        self.bids =[]
        self.winningBid = None
        self.winningIndex = None

    #fixLead
    def biddingPhase(self):
        players = self.gameCopy.players
        for p in players:
            bid = p.makeBid(self.getValidBidsForPlayer(p))
            self.bids.append(bid)
        winningTup= self.getWinningBid()
        self.winningBid = winningTup[0]
        self.winningIndex = winningTup[1]

    def getValidBidsForPlayer(self,player):
        hand = player.hand
        possibleModes = copy(MODES)
        suits = ['Eichel','Gras','Schellen']

        #Check for suits if person has the Ace if not check if he has at least one card of that suit that is not O or U
        for suit in suits:
            if Card(suit,'A') in hand:
                possibleModes.remove((1,SUITS[suit]))
                continue
            hasSuit = False
            for card in hand:
                if card.suit == suit and card.rank not in ['O','U']:
                    hasSuit = True
            if hasSuit == False:
                possibleModes.remove((1,SUITS[suit]))

        #Check to see if there are previous bids, if so remove all three Team games
        for bid in self.bids:
            a,_ = bid
            if a in [1,2,3]:
                #filters out all tuples (1,_)
                possibleModes = list(filter(lambda x: x[0]!=1,possibleModes))
        # print("Hand:{}\nPossibleBids:{}".format(hand,possibleModes))
        return possibleModes

    def getWinningBid(self):
        highestBid = max(self.bids,key=itemgetter(0))
        winningIndex = self.bids.index(highestBid)
        # print("Bid:{} \n HighestBid:{} \n Index: {}".format(self.bids,highestBid,winningIndex))
        return (highestBid,winningIndex)

    def getBids(self):
        return self.bids
