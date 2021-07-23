import os
import pickle
from torch.utils.tensorboard import SummaryWriter


# to allow for more easier training setting
class TrainSettings:
    def __init__(self, name, colab=True):
        self.name = name

        self.episodes = None
        self.update_games = None
        self.batch_size = None
        self.mini_batch_size = None
        self.K_epochs = None

        self.eval_rounds = None
        self.eval_interval = None

        self.checkpoints = None
        self.runsFolder = None

        self.summary_writer = None

        if colab:
            self.checkpoints = "/content/drive/MyDrive/experiment/" + self.name + "/checkpoints/"
            self.runsFolder = "/content/drive/MyDrive/experiment/" + self.name + "/runsFolder/"
            self.summary_writer = SummaryWriter(log_dir=self.runsFolder)
        else:
            self.runsFolder = os.getcwd() + "/PlayerModels/PPO/runsFolder/"
            self.checkpoints = os.getcwd() + "/PlayerModels/PPO/checkpoints/"
            self.summary_writer = SummaryWriter(log_dir=self.runsFolder)

    def save(self):
        with open(self.runsFolder + self.name, 'wb') as out:
            pickle.dump(self, out, pickle.HIGHEST_PROTOCOL)
