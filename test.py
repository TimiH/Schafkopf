from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer
# from PlayerModels.RandomSample import RandomSample
from Tournament import playFairTournament, playRandomTournament
from PlayerModels.PPO.LinearPolicy import LinearModel
from PlayerModels.ModelPlayer import ModelPlayer
import time

# p1 = RandomPlayer("RandomPlayer")
# 2v2
# p1 = HeuristicPlayer("HeuristicPlayer0")
# p2 = HeuristicPlayer("HeuristicPlayer1")
# p3 = RandomPlayer("RandomPlayer0")
# p4 = RandomPlayer("RandomPlayer1")
# 3v1
# p1 = HeuristicPlayer("HeuristicPlayer0")
# p2 = HeuristicPlayer("HeuristicPlayer1")
# p3 = HeuristicPlayer("HeuristicPlayer2")
# p4 = RandomPlayer("RandomPlayer0")

# p1 = HeuristicPlayer("HeuristicPlayer0")
# p2 = HeuristicPlayer("HeuristicPlayer1")
# p3 = HeuristicPlayer("HeuristicPlayer2")
# p4 = RandomPlayer("RandomPlayer0")

p1 = ModelPlayer('Mode0', LinearModel(), eval=True)
p2 = ModelPlayer('Model', LinearModel(), eval=True)
p3 = ModelPlayer('Mode2', LinearModel(), eval=True)
p4 = ModelPlayer('Mode3', LinearModel(), eval=True)

# #4H
# p1 = HeuristicPlayer("HeuristicPlayer0")
# p2 = HeuristicPlayer("HeuristicPlayer1")
# p3 = HeuristicPlayer("HeuristicPlayer2")
# p4 = HeuristicPlayer("HeuristicPlayer3")


players = [p1, p2, p3, p4]
start = time.time()
stats = playFairTournament(players, 100, laufendeBool=False)
# stats = playRandomTournament(players, 1000,laufendeBool=False)
end = time.time()
print(("Time:", end - start))
