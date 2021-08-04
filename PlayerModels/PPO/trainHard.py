from PlayerModels.PPO.trainSettings import TrainSettings
from PlayerModels.PPO.trainRL import main

tSettings = TrainSettings('a001', colab=False)

tSettings.episodes = 200
tSettings.eval_rounds = 1000
tSettings.eval_interval = 5

tSettings.update_games = 100000
tSettings.batch_size = tSettings.update_games * 8 * 4
tSettings.mini_batch_size = tSettings.batch_size

tSettings.K_epochs = 8

# tSettings.save()
main(tSettings)
