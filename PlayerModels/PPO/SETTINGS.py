import logging
import os
import os
import torch
from torch.utils.tensorboard import SummaryWriter


# from dataset import ExperienceDatasetLinear, ExperienceDatasetLSTM
# from PlayerModels.PPO.LinearPolicy import LinearModel

class Settings:
    # global logger
    logger = logging.getLogger(__name__)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)

    # Tensorboard
    runFolder = os.getcwd() + "/runsFolder/"
    summary_writer = SummaryWriter(log_dir=runFolder)

    # Parameters
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    update_games = 10000  # update policy every n games
    batch_size = update_games * 22
    mini_batch_size = batch_size
    eval_games = 500
    checkpoint_folder = os.getcwd() + "/checkpoints/"

    lr = 0.0002
    lr_stepsize = 30000000  # 300000
    lr_gamma = 0.3

    betas = (0.9, 0.999)
    gamma = 0.99  # discount factor
    K_epochs = 16  # 8  # update policy for K epochs
    eps_clip = 0.2  # clip parameter for PPO
    c1, c2 = 0.5, 0.005

    optimizer_weight_decay = 1e-5

    random_seed = None
