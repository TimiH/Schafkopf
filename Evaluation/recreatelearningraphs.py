import pickle
import pandas as pd
import matplotlib.pyplot as plt

# path = './' + '15kcom.p'
path = '/home/tim/Work/Schafkopf/DataDump/15kcom.p'
with open(path, 'rb') as handle:
    b = pickle.load(handle)
evPlayerHeu = []
evHeu = []
winHeu = []
winPlayerHeu = []
evPlayerGre = []
evGre = []
winGre = []
winPlayerGre = []
evPlayerRan = []
evRan = []
winRan = []
winPlayerRan = []
l = {}
lPer = {}
games = ['Wenz', 'Solo', "Team", "Team-Partmer", 'Sauspiel-Opp', "Wenz-Opp", "Solo-Opp"]
player = ['evPlayerHeu', 'evPlayerGre', 'evPlayerRan']
playerPer = ['evPlayerPerHeu', 'evPlayerPerGre', 'evPlayerPerRan']
for d in b:
    for k in games:
        if k not in l:
            l[k] = []
            lPer[k] = []

        tmp = []
        for kk in player:
            tmp.append(d[kk][k])
        l[k].append(tmp)
        tmp = []
        for kk in playerPer:
            tmp.append(d[kk][k])
        lPer[k].append(tmp)
    evPlayerHeu.append(d['evPlayerHeu'])
    evHeu.append(d['evPlayerHeu'])
    winHeu.append(d['evOverallPerHeu'])
    winPlayerHeu.append(d['evPlayerPerHeu'])
    evPlayerGre.append(d['evPlayerGre'])
    evGre.append(d['evPlayerGre'])
    winGre.append(d['evOverallPerGre'])
    winPlayerGre.append(d['evPlayerPerGre'])
    evPlayerRan.append(d['evPlayerRan'])
    evRan.append(d['evPlayerRan'])
    winRan.append(d['evOverallPerRan'])
    winPlayerRan.append(d['evPlayerPerRan'])

for k, v in l.items():
    l[k] = pd.DataFrame(v, columns=player)
for k, v in lPer.items():
    lPer[k] = pd.DataFrame(v, columns=playerPer)
df = pd.DataFrame.from_dict(b)
df.index = list(map(lambda x: int(x * 5), list(df.index)))
df_overall = df.rename(columns={"evOverallPerHeu": "Heuristic", "evOverallPerGre": "Greedy",
                                "evOverallPerRan": "Random"})
df_overall[['Heuristic', 'Random', 'Greedy']].plot(ylabel="Winrate %", xlabel="Episode",
                                                   grid=True, title="")
# plt.savefig('evOverall.png')
# plt.show()

# USE THIS FOR MORE GRANULAR TICKS
# df_overall[['Heuristic Model','Random Model','Greedy Model']].plot(ylabel="Evaluation Function", xlabel="Episode", grid=True, title="", xticks=df_overall.index)


for game in games:
    df = l[game].rename(
        columns={"evPlayerHeu": "Heuristic", "evPlayerGre": "Greedy", "evPlayerRan": "Random"})
    df.plot(title=game, xlabel='Episode', ylabel='Expected Value')
for game in games:
    df = lPer[game].rename(columns={"evPlayerPerHeu": "Heuristic", "evPlayerPerGre": "Greedy",
                                    "evPlayerPerRan": "Random"})
    df.plot(title=game + "Per", xlabel='Episode', ylabel='Winrate %')

plt.show()
