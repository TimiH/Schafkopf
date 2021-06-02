from PlayerModels.RandomPlayer import RandomPlayer

from Tournament import playFairTournament
import time

# p1 = RandomSample("Tim")
p1 = RandomPlayer("1", True, 'randomdata.csv')
p2 = RandomPlayer("2")
p3 = RandomPlayer("3")
p4 = RandomPlayer("4")

players = [p1, p2, p3, p4]
# g = Game(players,0)
# g.mainGame()
# start = time.time()
playFairTournament(players, 100)
end = time.time()
# print("Time:", end-start)
