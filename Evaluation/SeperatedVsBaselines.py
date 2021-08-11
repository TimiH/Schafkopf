from Tournament import playFairTournament
from PlayerModels.PPO.util import loadSeperatedPlayer, loadLinearPlayer
from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer
from PlayerModels.GreedyPlayer import GreedyPlayer

rounds = 2500

# p1 = loadLinearPlayer('CompleteRL1', '15ComA', 111)
# p3 = loadLinearPlayer('CompleteRL2', '15ComA', 111)
p1 = loadSeperatedPlayer('SeperateRL1', '500sad', 100)
p3 = loadSeperatedPlayer('SeperateRL2', '500sad', 100)
# Heuristic
p2 = HeuristicPlayer("heu1")
p4 = HeuristicPlayer("heu2")

df0 = playFairTournament([p1, p2, p3, p4], rounds, laufendeBool=False, verbose=False)
print(f'Heuristic: {df0.getEVOverall()}')

# # Random
# p2 = RandomPlayer('rand1')
# p4 = RandomPlayer('rand2')
# df1 = playFairTournament([p1, p2, p3, p4], rounds, laufendeBool=False, verbose=False)
# print(f'Random: {df1.getEVOverall()}')

# # Greedy
# p2 = GreedyPlayer('Greedy1')
# p4 = GreedyPlayer('Greedy2')
# df2 = playFairTournament([p1, p2, p3, p4], rounds, laufendeBool=False, verbose=False)
# print(f'Random: {df2.getEVOverall()}')
