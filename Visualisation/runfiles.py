import glob
import pandas as pd
import matplotlib.pyplot as plt
import torch

path = '/home/tim/Work/Schafkopf/PlayerModels/PPO/experiments/runsFolder/'
name = '15ComA'

fullpath = path + name + '/data/*.json'
files = glob.glob(fullpath)

dfval = pd.read_json(files[0]).drop(columns=0)
dfpol = pd.read_json(files[1]).drop(columns=0)
dfvar = pd.read_json(files[2]).drop(columns=0)
dfent = pd.read_json(files[3]).drop(columns=0)

# plot
plt.plot(dfval[1], dfval[2], color='tab:blue')
plt.plot(dfpol[1], dfpol[2], color='tab:orange')

plt.plot(dfvar[1], dfvar[2], color='tab:purple')
plt.plot(dfent[1], dfent[2], color='tab:green')
plt.xlim(0)
plt.grid()
