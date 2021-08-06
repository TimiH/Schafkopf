from PlayerModels.PPO.trainSettings import TrainSettings
from PlayerModels.PPO.trainRLseperated import main

name = '133'

episodes = 250
eval_rounds = 250
eval_interval = 5
update_games = 300
lr_stepsize = 10000000

# tSettings = TrainSettings(name, colab=False, seperated=1)
# tSettings.episodes = episodes
# tSettings.eval_rounds = eval_rounds
# tSettings.eval_interval = eval_interval  # error 10
# tSettings.lr_stepsize = lr_stepsize
# tSettings.update_games = update_games
# tSettings.batch_size = tSettings.update_games * 8 * 4
# tSettings.mini_batch_size = tSettings.batch_size
# tSettings.K_epochs = 12
#
# # tSettings.save()
# main(tSettings, mode=1)
#
# tSettings = TrainSettings(name, colab=False, seperated=2)
# tSettings.episodes = episodes
# tSettings.eval_rounds = eval_rounds
# tSettings.eval_interval = eval_interval  # error 10
# tSettings.lr_stepsize = lr_stepsize
# tSettings.update_games = update_games
# tSettings.batch_size = tSettings.update_games * 8 * 4
# tSettings.mini_batch_size = tSettings.batch_size
# tSettings.K_epochs = 12

# tSettings.save()
# main(tSettings, mode=2)

tSettings = TrainSettings(name, colab=False, seperated=3)
tSettings.episodes = episodes
tSettings.eval_rounds = eval_rounds
tSettings.eval_interval = eval_interval  # error 10
tSettings.lr_stepsize = lr_stepsize
tSettings.update_games = update_games
tSettings.batch_size = tSettings.update_games * 8 * 4
tSettings.mini_batch_size = tSettings.batch_size

tSettings.K_epochs = 12

# tSettings.save()
main(tSettings, mode=3)
