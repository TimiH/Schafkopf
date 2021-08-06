import os
import sys

from PlayerModels.PPO.trainSettings import TrainSettings
from PlayerModels.PPO.trainRL import main

tSettings = TrainSettings('test', colab=False)

tSettings.episodes = 200
tSettings.eval_rounds = 5000
tSettings.eval_interval = 5
tSettings.lr_stepsize = 30000000
tSettings.update_games = 8000
tSettings.batch_size = int(tSettings.update_games * 8 * 4 * 0.8)
tSettings.mini_batch_size = tSettings.batch_size

tSettings.K_epochs = 16

# tSettings.save()
main(tSettings)
