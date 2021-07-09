from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer
# from PlayerModels.RandomSample import RandomSample
from Tournament import playFairTournament, playRandomTournament
import time

# p1 = RandomPlayer("RandomPlayer")
# 2v2
# p1 = HeuristicPlayer("HeuristicPlayer0")
# p2 = HeuristicPlayer("HeuristicPlayer1")
# p3 = RandomPlayer("RandomPlayer0")
# p4 = RandomPlayer("RandomPlayer1")
# 3v1
p1 = HeuristicPlayer("HeuristicPlayer0")
p2 = HeuristicPlayer("HeuristicPlayer1")
p3 = HeuristicPlayer("HeuristicPlayer2")
p4 = RandomPlayer("RandomPlayer0")


# #4H
# p1 = HeuristicPlayer("HeuristicPlayer0")
# p2 = HeuristicPlayer("HeuristicPlayer1")
# p3 = HeuristicPlayer("HeuristicPlayer2")
# p4 = HeuristicPlayer("HeuristicPlayer3")

players = [p1, p2, p3, p4]
start = time.time()
stats = playFairTournament(players, 2500, laufendeBool=False)
# stats = playRandomTournament(players, 1000,laufendeBool=False)
end = time.time()
print(("Time:", end - start))
