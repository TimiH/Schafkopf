from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer
# from PlayerModels.RandomSample import RandomSample
from PlayerModels.Player import Player
from PlayerModels.GreedyPlayer import GreedyPlayer
from Tournament import playFairTournament, playRandomTournament
from PlayerModels.PPO.LinearPolicy import LinearModel
from PlayerModels.PPO.SoloPolicy import SoloModel
from PlayerModels.ModelPlayer import ModelPlayer
from PlayerModels.SeperatedModelPlayer import SeperatedModelPlayer
import time
import torch

# p1 = RandomPlayer("RandomPlayer")
# # 2
p1 = HeuristicPlayer("HeuristicPlayer0")
p3 = GreedyPlayer("RandomPlayer0")
p2 = HeuristicPlayer("HeuristicPlayer1")
p4 = GreedyPlayer("RandomPlayer1")
# 3v1
# p1 = HeuristicPlayer("HeuristicPlayer0")
# p2 = HeuristicPlayer("HeuristicPlayer1")
# p3 = HeuristicPlayer("HeuristicPlayer2")
# p4 = RandomPlayer("RandomPlayer0")

p1 = HeuristicPlayer("HeuristicPlayer0")
p2 = RandomPlayer("RandomPlayer0")
p3 = HeuristicPlayer("HeuristicPlayer2")
p4 = RandomPlayer("RandomPlayer0")

# p1 = ModelPlayer('Mode0', LinearModel(), eval=True)
# p2 = ModelPlayer('Model', LinearModel(), eval=True)
# p3 = ModelPlayer('Mode2', LinearModel(), eval=True)
# p4 = ModelPlayer('Mode3', LinearModel(), eval=True)

# #4H
# p1 = HeuristicPlayer("HeuristicPlayer1")
# p2 = HeuristicPlayer("HeuristicPlayer2")
# p3 = HeuristicPlayer("HeuristicPlayer3")
# p4 = HeuristicPlayer("HeuristicPlayer4")

# p1 = GreedyPlayer("greedy")
# p2 = RandomPlayer("RandomPlayer1")
# p3 = RandomPlayer("RandomPlayer2")
# p4 = RandomPlayer("RandomPlayer3")

# soloModel = SoloModel()
# soloModel.load_state_dict(torch.load('PlayerModels/PPO/checkpoints/runSample/873.pt',map_location=torch.device('cpu')))

# p1 = SeperatedModelPlayer('Solo0',policySolo=soloModel,eval=True)
# p3 = SeperatedModelPlayer('Solo3',policySolo=soloModel,eval=True)
players = [p1, p2, p3, p4]
start = time.time()
stats = playFairTournament(players, 2500, mode=0, verbose=True, laufendeBool=False)
# stats = playRandomTournament(players, 200, mode=3, laufendeBool=False)
end = time.time()
print(("Time:", end - start))
