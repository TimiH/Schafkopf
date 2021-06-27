from Deck import Deck
from Card import Card
from Player import Player
from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer
# from PlayerModels.RandomSample import RandomSample

from Game import Game
from Bidding import Bidding
from Trick import Trick
from Tournament import playTournament, playFairTournament
import time

# p1 = RandomSample("Tim")
p1 = HeuristicPlayer("1")
p2 = HeuristicPlayer("2")
p3 = HeuristicPlayer("3")
p4 = HeuristicPlayer("4")

players = [p1, p2, p3, p4]
start = time.time()
playFairTournament(players, 10000)
end = time.time()
print(("Time:", end - start))
