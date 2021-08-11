from Tournament import playFairTournament
from PlayerModels.PPO.util import loadSeperatedPlayer, loadLinearPlayer
from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer

rounds = 2500

p1 = loadSeperatedPlayer('SeperateRL1', '500sad', 100)
p3 = loadSeperatedPlayer('SeperateRL2', '500sad', 100)

# Heuristic
p2 = loadLinearPlayer('ComleteRL1', "15ComA", 111)
p4 = loadLinearPlayer('ComleteRL2', "15ComA", 111)

df0 = playFairTournament([p1, p2, p3, p4], rounds, laufendeBool=False, verbose=False)
print(f'Heuristic: {df0.getEVOverall()}')
