from Tournament import playFairTournament
from PlayerModels.PPO.util import loadSeperatedPlayer, loadLinearPlayer
from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer

rounds = 2500

p1 = loadSeperatedPlayer('Sep1', 132, 500)
p3 = loadSeperatedPlayer('Sep2', 132, 500)

# Heuristic
p2 = loadLinearPlayer('Lin1', 2000, 21)
p4 = loadLinearPlayer('Lin2', 2000, 21)

df0 = playFairTournament([p1, p2, p3, p4], rounds, laufendeBool=False, verbose=False)
print(f'Heuristic: {df0.getEVOverall()}')
