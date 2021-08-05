from PlayerModels.PPO.trainSettings import TrainSettings
from PlayerModels.PPO.trainRLseperated import main

tSettings = TrainSettings('131', colab=False)

tSettings.episodes = 200
tSettings.eval_rounds = 1000
tSettings.eval_interval = 10000  # error 10
tSettings.lr_stepsize = 30000000
tSettings.update_games = 200
tSettings.batch_size = tSettings.update_games * 8 * 4
tSettings.mini_batch_size = tSettings.batch_size

tSettings.K_epochs = 12

# tSettings.save()
main(tSettings, mode=1)

tSettings = TrainSettings('131', colab=False)

tSettings.episodes = 200
tSettings.eval_rounds = 1000
tSettings.eval_interval = 10000  # error 10
tSettings.lr_stepsize = 30000000
tSettings.update_games = 200
tSettings.batch_size = tSettings.update_games * 8 * 4
tSettings.mini_batch_size = tSettings.batch_size

tSettings.K_epochs = 12

# tSettings.save()
main(tSettings, mode=2)

tSettings = TrainSettings('132', colab=False)

tSettings.episodes = 200
tSettings.eval_rounds = 1000
tSettings.eval_interval = 10000  # error 10
tSettings.lr_stepsize = 30000000
tSettings.update_games = 200
tSettings.batch_size = tSettings.update_games * 8 * 4
tSettings.mini_batch_size = tSettings.batch_size

tSettings.K_epochs = 12

# tSettings.save()
main(tSettings, mode=3)
