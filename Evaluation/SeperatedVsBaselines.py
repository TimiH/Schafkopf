from Tournament import playFairTournament
from PlayerModels.PPO.util import loadSeperatedPlayer
from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer

rounds = 2500

p1 = loadSeperatedPlayer('Sep1', 132, 500)
p3 = loadSeperatedPlayer('Sep2', 132, 500)

# Heuristic
p2 = HeuristicPlayer("heu1")
p4 = HeuristicPlayer("heu2")

df0 = playFairTournament([p1, p2, p3, p4], rounds, laufendeBool=False, verbose=False)
print(f'Heuristic: {df0.getEVOverall()}')

# Random
p2 = RandomPlayer('rand1')
p4 = RandomPlayer('rand2')
df1 = playFairTournament([p1, p2, p3, p4], rounds, laufendeBool=False, verbose=False)
print(f'Random: {df1.getEVOverall()}')
