from PlayerModels.PPO.trainSettings import TrainSettings
from PlayerModels.PPO.trainRLseperated import main

name = '500SepA'
episodes = 100
eval_rounds = 500
eval_interval = 100
update_games = 500
lr_stepsize = 30000000
K_epochs = 8

tSettings = TrainSettings(name, colab=False, seperated=1)
tSettings.episodes = episodes
tSettings.eval_rounds = eval_rounds
tSettings.eval_interval = eval_interval  # error 10
tSettings.lr_stepsize = lr_stepsize
tSettings.update_games = update_games
tSettings.batch_size = int(tSettings.update_games * 8 * 4 * 0.8)
tSettings.mini_batch_size = tSettings.batch_size
tSettings.K_epochs = K_epochs

main(tSettings, mode=1)
#
# tSettings = TrainSettings(name, colab=False, seperated=2)
# tSettings.episodes = episodes
# tSettings.eval_rounds = eval_rounds
# tSettings.eval_interval = eval_interval  # error 10
# tSettings.lr_stepsize = lr_stepsize
# tSettings.update_games = update_games
# tSettings.batch_size = int(tSettings.update_games * 8 * 4 * 0.8)
# tSettings.mini_batch_size = tSettings.batch_size
# tSettings.K_epochs = K_epochs
#
# main(tSettings, mode=2)
#
# tSettings = TrainSettings(name, colab=False, seperated=3)
# tSettings.episodes = episodes
# tSettings.eval_rounds = eval_rounds
# tSettings.eval_interval = eval_interval  # error 10
# tSettings.lr_stepsize = lr_stepsize
# tSettings.update_games = update_games
# tSettings.batch_size = int(tSettings.update_games * 8 * 4 * 0.8)
# tSettings.mini_batch_size = tSettings.batch_size
#
# tSettings.K_epochs = K_epochs
#
# main(tSettings, mode=3)
