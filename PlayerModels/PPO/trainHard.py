import os
import sys

from PlayerModels.PPO.trainSettings import TrainSettings
from PlayerModels.PPO.trainRL import main

tSettings = TrainSettings('125', colab=False)

tSettings.episodes = 200
tSettings.eval_rounds = 1000
tSettings.eval_interval = 10000  # error 10
tSettings.lr_stepsize = 10000000
tSettings.update_games = 200
tSettings.batch_size = tSettings.update_games * 8 * 4
tSettings.mini_batch_size = tSettings.batch_size

tSettings.K_epochs = 12

# tSettings.save()
main(tSettings)
