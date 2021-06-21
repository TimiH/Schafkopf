import glob
import os
import numpy
import pickle
import pandas as pd
from bitarray import bitarray
import matplotlib.pyplot as plt

files = glob.glob(os.getcwd() + '/DataDump/' + '*.p')

data = []
for g in files:
    hand = open(g, 'rb')
    handDict = pickle.load(hand)

    for trick in handDict:
        d = handDict[trick]
        row = []
        row.append(sum(bitarray(d['Hand'])))
        row.append(sum(bitarray(d['ValidCards'])))
        row.append(d['GameMode'][0])
        row.append(d['Lead'] == d['PostionMeTable'])
        data.append(row)

df = pd.DataFrame(data)
df = df.rename(columns={0: 'Trick#', 1: 'Actions', 2: 'GameMode', 3: 'Lead'})
df = df.astype({"Lead": bool, "GameMode": 'category'})

# Plotting
# groupby Trick

# avg Trick
