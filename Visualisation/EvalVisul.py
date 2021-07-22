from Tournament import playFairTournament
from PlayerModels.ModelPlayer import ModelPlayer
from PlayerModels.PPO.LinearPolicy import LinearModel
from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer

import torch
import os
import glob
import re

path = '/home/tim/Work/Schafkopf/PlayerModels/PPO/checkpoints/'
# collect all generations and sort
generations = glob.glob(path + '*.pt')
generations.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))
# for each epoch play Heuristic,Random
for gen in generations:
    genNumber = int(re.findall(r'\d+', gen)[0])
    # Load Policy and create Players
    policy = LinearModel()
    policy.load_state_dict(torch.load(gen))

    # players sit at 0,2
    p0 = ModelPlayer('mod0', policy, eval=True)
    p2 = ModelPlayer('mod2', policy, eval=True)

# collect df.EVoverall df.Player
# mean both and attach to df.
