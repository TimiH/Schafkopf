import pickle
import pandas as pd
import glob
import os
from scipy.stats import f_oneway

#Loading Files
path = os.getcwd() + '/pickleData/BAAA/' + 'BAAA*'
files = glob.glob(path)

#DataAggregatiom
dfEvOverall = None
dfEvPlayer = None

for key, f in enumerate(files):
    pick = open(f, 'rb')
    stats = pickle.load(pick)
    dfEvOverallTemp = stats.getEVOverall()
    dfEvPlayerTemp = stats.getEVGameModePlayers()
    if key == 0:
        dfEvOverall = dfEvOverallTemp
        dfEvPlayer = dfEvPlayerTemp
    else:
        dfEvOverall = pd.concat([dfEvOverall, dfEvOverallTemp], ignore_index=True)
        dfEvPlayer = pd.concat([dfEvPlayer,dfEvPlayerTemp])
#cleanup
# del dfEvOverallTemp
# del dfEvPlayerTemp

#Renaming and organising
#Players sit Weak,Strong,Strong,Strong,[r0,h1,h2,h3]
cnames = {'r0': 'WeakBehind', 'h1': 'Strong+1', 'h2': 'Strong+2', 'h3': 'Strong+3'}
dfEvOverall = dfEvOverall.rename(columns=cnames)
dfEvPlayer = dfEvPlayer.groupby(dfEvPlayer.index).mean().rename(index=cnames)
# stats part

#F, p = f_oneway(dfEvOverall['WeakBehind'], dfEvOverall['WeakOpp'], dfEvOverall['WeakInFront'])

