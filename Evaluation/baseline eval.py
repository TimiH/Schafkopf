from Tournament import playFairTournament
from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.GreedyPlayer import GreedyPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer

rounds = 2500

players = [RandomPlayer(str(i)) for i in range(4)]
df0 = playFairTournament(players, rounds, laufendeBool=False, verbose=False)
per0 = df0.getWinPercentagesPlayer().mean(axis=0).round(3).to_frame().transpose().to_latex()

players = [GreedyPlayer(str(i)) for i in range(4)]
df1 = playFairTournament(players, rounds, laufendeBool=False, verbose=False)
per1 = df1.getWinPercentagesPlayer().mean(axis=0).round(3).to_frame().transpose().to_latex()

players = [HeuristicPlayer(str(i)) for i in range(4)]
df2 = playFairTournament(players, rounds, laufendeBool=False, verbose=False)
per2 = df2.getWinPercentagesPlayer().mean(axis=0).round(3).to_frame().transpose().to_latex()
