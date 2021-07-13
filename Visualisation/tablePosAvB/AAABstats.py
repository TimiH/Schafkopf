import pickle
import pandas as pd
import glob
import os
from scipy.stats import f_oneway

#Loading Files
path = os.getcwd() + '/pickleData/ABBB/' + 'ABBB*'
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
#players = [h1,r1,r2,r3]
cnames = {'h1':'Strong','r1':'Weak+1','r2':'Weak+2','r3':'Weak+3'}
dfEvOverall = dfEvOverall.rename(columns=cnames)
dfEvOverallMean = dfEvOverall.mean().round(2)
dfEvPlayer = dfEvPlayer.groupby(dfEvPlayer.index).mean().rename(index=cnames).round(2)
# stats part

#F, p = f_oneway(dfEvOverall['WeakBehind'], dfEvOverall['WeakOpp'], dfEvOverall['WeakInFront'])

