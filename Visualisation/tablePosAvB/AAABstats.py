import pickle
import pandas as pd
import glob
import os
from scipy.stats import f_oneway

path = os.getcwd() + '/pickleData/ABBB/' + 'ABBB*'
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

cnames = {'h1': 'StrongPlayer', 'r1': 'WeakBehind', 'r2': 'WeakOpp', 'r3': 'WeakInFront'}
df = df.rename(columns=cnames)

# stats part
df.describe()
F, p = f_oneway(df['WeakBehind'], df['WeakOpp'], df['WeakInFront'])
