import os
import pickle
from torch.utils.tensorboard import SummaryWriter


# to allow for more easier training setting
class TrainSettings:
    def __init__(self, name, colab=True):
        self.name = name
        self.colab = colab

        self.episodes = None
        self.update_games = None
        self.batch_size = None
        self.mini_batch_size = None
        self.lr_stepsize = None
        self.K_epochs = None

        self.eval_rounds = None
        self.eval_interval = None

        self.checkpoints = None
        self.runsFolder = None

        self.summary_writer = None

        if self.colab:
            self.checkpoints = "/content/drive/MyDrive/experiment/" + self.name + "/checkpoints/"
            self.runsFolder = "/content/drive/MyDrive/experiment/" + self.name + "/runsFolder/"
            self.summary_writer = SummaryWriter(log_dir=self.runsFolder)
        else:
            self.runsFolder = os.getcwd() + "/PlayerModels/PPO/runsFolder/"
            self.checkpoints = os.getcwd() + "/PlayerModels/PPO/checkpoints/"
            self.summary_writer = SummaryWriter(log_dir=self.runsFolder)

    def save(self):
        data = {
            'name': self.name,
            'colab': self.colab,
            'episodes': self.episodes,
            'update_ games': self.update_games,
            'batch_size': self.batch_size,
            'mini_batches': self.mini_batch_size,
            'K_epochs': self.K_epochs,
            'lr_stepsize': self.lr_stepsize,
            'eval_rounds': self.eval_rounds,
            'eval_intervals': self.eval_interval,
        }
        with open(self.runsFolder + self.name, 'wb') as out:
            pickle.dump(data, out, pickle.HIGHEST_PROTOCOL)

    def load(path):
        with open(path, 'rb') as data:
            d = pickle.load(data)
        pass
