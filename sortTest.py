from Deck import Deck
from CardValues import SUITS,RANKS,VALUES
from Card import Card
from helper import sortHand
from helper import byRank, bySuit,bySuitRank


d = Deck()
#d.cards = list(filter(lambda x: x.rank == 'O' or x.rank == 'U', d.cards))
d.shuffle()
hand = d.deal(8)

sortedHand = sorted(hand,key=(bySuitRank))
print(sortedHand)
