import pandas
from Tournament import playBaseLineTournament
from PlayerModels.PPO.util import loadSeperatedPlayer, loadLinearPlayer

start = 1
end = 100
interval = 5
name = '15CompleteRL'
experiment = '15ComA'
rounds = 2000

winOverallHeu = []
winPlayerHeu = []
evOverallHeu = []
evPlayerHeu = []
winOverallRan = []
winPlayerRan = []
evOverallRan = []
evPlayerRan = []
winOverallGre = []
winPlayerGre = []
evOverallGre = []
evPlayerGre = []
dataTotal = []
for i in range(start, end):
    if i % interval == 0:
        print(f'Playing{i}')
        # p1 = loadSeperatedPlayer(name+'1',experiment,i)
        # p2 = loadSeperatedPlayer(name+'3',experiment,i)
        p1 = loadLinearPlayer(name + '1', experiment, i)
        p2 = loadLinearPlayer(name + '3', experiment, i)
        players = [p1, p2]
        data = playBaseLineTournament(players, rounds, mode=0)
        dataTotal.append(data)
        # statsDict = {
        #     'evOverallHeu': evOverallHeu,
        #     'evPlayerHeu': evPlayerHeu,
        #     'evOverallPerHeu': evOverallPerHeu,
        #     'evPlayerPerHeu': evPlayerPerHeu,
        #     'evOverallRan': evOverallRan,
        #     'evPlayerRan': evPlayerRan,
        #     'evOverallPerRan': evOverallPerRan,
        #     'evPlayerPerRan': evPlayerPerRan,
        #     'evOverallGre': evOverallGre,
        #     'evPlayerGre': evPlayerGre,
        #     'evOverallPerGre': evOverallPerGre,
        #     'evPlayerPerGre': evPlayerPerGre
        # }
