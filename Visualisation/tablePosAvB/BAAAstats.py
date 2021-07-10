import pickle
import pandas as pd
import glob
import os
from scipy.stats import f_oneway

path = os.getcwd() + '/pickleData/BAAA/' + 'BAAA*'
files = glob.glob(path)
df = None

for key, f in enumerate(files):
    pick = open(f, 'rb')
    stats = pickle.load(pick)
    dfTemp = stats.getEVOverall()
    if key == 0:
        df = dfTemp
    else:
        df = pd.concat([df, dfTemp], ignore_index=True)

cnames = {'r1': 'WeakPlayer', 'h1': 'StrongBehind', 'ph2': 'StrongOpp', 'ph3': 'StrongInFront'}
df = df.rename(columns=cnames)

# stats
F, p = f_oneway(df['StrongBehind'], df['StrongOpp'], df['StrongInFront'])
