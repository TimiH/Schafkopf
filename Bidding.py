import CardValues
import GameModes
from operator import itemgetter

class Bidding:
    def __init__(self, gameCopy):
        self.gameCopy = gameCopy
        self.bids =[]
        self.winningBid = None
        self.winningIndex = None

    def biddingPhase(self):
        players = self.gameCopy.players
        for p in players:
            bid = p.makeBid(getValidBidsForPlayer(p))
            self.bids.append(bid)
        self.winningBid, self.winninnIndex = getWinningBid()

    def getValidBidsForPlayer(self,player):
        hand = player.hand
        possibleModes = MODES
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
        for bid in bids:
            a,_ = bid
            if a in [1,2,3]:
                possibleModes.remove(bid)
        return possibleModes

        def getWinningBid(self):
            highestBid = max(self.bids,key=itemgetter(0))
            indexWinningIndex = self.bids.index[highestBid]
            return (highestBid,indexWinningIndex)
