from Tournament import playFairTournament
from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.GreedyPlayer import GreedyPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer

rounds = 2500
ran = [RandomPlayer(str(i)) for i in range(2)]
greed = [GreedyPlayer(str(i)) for i in range(2)]
heur = [HeuristicPlayer(str(i)) for i in range(2)]

# #Random vs Greed
# players = [ran[0],greed[0],ran[1],greed[1]]
# df0 = playFairTournament(players, rounds, laufendeBool=False, verbose=False)
# per0 = df0.getWinPercentagesPlayer().mean(axis=0).round(3).to_frame().transpose().to_latex()
#
# #Random vs Heur
# players = [ran[0],heur[0],ran[1],heur[1]]
# df1 = playFairTournament(players, rounds, laufendeBool=False, verbose=False)
# per1 = df1.getWinPercentagesPlayer().mean(axis=0).round(3).to_frame().transpose().to_latex()

# greed vs Heur
players = [greed[0], heur[0], greed[1], heur[1]]
df2 = playFairTournament(players, rounds, laufendeBool=False, verbose=False)
per2 = df2.getWinPercentagesPlayer().mean(axis=0).round(3).to_frame().transpose().to_latex()
