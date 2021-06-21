from CardValues import SUITS
from GameModes import MODES
from operator import itemgetter
from Card import Card
from copy import deepcopy,copy

class Bidding:
    def __init__(self, gameDict, lead):
        self.gameDict = gameDict
        self.bids = []
        self.winningBid = None
        self.winningIndex = None
        self.lead = self.gameDict['leadingPlayer']

    # fixLead
    def biddingPhase(self):
        players = self.gameDict['players']
        while not self.isFinished():
            self.nextAction()
        winningTup = self.getWinningBid()
        self.winningBid = winningTup[0]
        self.winningIndex = winningTup[1]

    def nextAction(self):
        players = self.gameDict['players']
        currentPlayerIndex = (len(self.bids) + self.lead) % 4
        playerhand = self.gameDict['playersHands'][currentPlayerIndex]
        p = players[currentPlayerIndex]
        p.setHand(playerhand)
        bid = p.makeBid(self.getValidBidsForPlayer(p))
        self.bids.append(bid)

    def isFinished(self):
        if len(self.bids) == 4:
            return True
        else:
            return False

    def getValidBidsForPlayer(self, player):
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
            if bid == (None,None):
                continue
            a = bid[0]
            if a in [1,2,3]:
                #filters out all tuples (1,_)
                possibleModes = list([x for x in possibleModes if x[0] != 1])
                break
        # print("Hand:{}\nPossibleBids:{}".format(hand,possibleModes))
        return possibleModes

    def getWinningBid(self):
        #print ("WinningBid:",self.bids)
        highestBid = max(self.bids,key=itemgetter(0))
        winningBidIndex = self.bids.index(highestBid)
        winningIndex = (winningBidIndex + self.lead)%4
        return (highestBid,winningIndex)

    def getBids(self):
        return self.bids
