from Tournament import playFairTournament
from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer
import pandas as pd
import pickle
import os

for run in range(30):
    #Run 30*10k BAAA
    h1,h2,h3 = HeuristicPlayer('h1'),HeuristicPlayer('h2'),HeuristicPlayer('h3')
    r0 = RandomPlayer('r1')
    players = [r0,h1,h2,h3]
    name = '/pickleData/BAAA/BAAA'+str(run)
    stats = playFairTournament(players, 2500, laufendeBool=False)
    with open(os.getcwd() + name, 'wb') as out:
        pickle.dump(stats, out, pickle.HIGHEST_PROTOCOL)

for run in range(30):
    #Run 30*10k ABBB
    r1,r2,r3 = RandomPlayer('r1'),RandomPlayer('r2'),RandomPlayer('r3')
    h1 = HeuristicPlayer('h1')
    players = [h1,r1,r2,r3]
    name = '/pickleData/ABBB/ABBB'+str(run)
    stats = playFairTournament(players, 2500, laufendeBool=False)
    with open(os.getcwd() + name, 'wb') as out:
        pickle.dump(stats, out, pickle.HIGHEST_PROTOCOL)

# for run in range(30):
#     # Run 30*10k AABB
#     r1, r2, h1, h2 = RandomPlayer('r1'), RandomPlayer('r1'), HeuristicPlayer('h1'), HeuristicPlayer('h2')
#     players = [r1, r2, h1, h2]
#     name = '/pickleData/AABB/AABB' + str(run)
#     stats = playFairTournament(players, 2500, laufendeBool=False)
#     with open(os.getcwd() + name, 'wb') as out:
#         pickle.dump(stats, out, pickle.HIGHEST_PROTOCOL)
#
# for run in range(30):
#     # Run 30*10k AABB
#     r1, r2, h1, h2 = RandomPlayer('r1'), RandomPlayer('r1'), HeuristicPlayer('h1'), HeuristicPlayer('h2')
#     players = [r1, h1, r1, h2]
#     name = '/pickleData/ABAB/ABAB' + str(run)
#
#     stats = playFairTournament(players, 2500, laufendeBool=False)
#     with open(os.getcwd() + name, 'wb') as out:
#         pickle.dump(stats, out, pickle.HIGHEST_PROTOCOL)
