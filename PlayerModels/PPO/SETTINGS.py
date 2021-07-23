import logging
import os
import torch
from torch.utils.tensorboard import SummaryWriter


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
    runFolder = os.getcwd() + "/PlayerModels/PPO/runsFolder/"
    checkFolder = os.getcwd() + "/PlayerModels/PPO/checkpoints/"

    # summary_writer = SummaryWriter(log_dir=runFolder)
    device = None
    # Parameters
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    # episodes = 200
    # update_games = 1000  # update policy every n games
    # batch_size = update_games * 4 * 8  # 4 players * 8 tuples
    # mini_batch_size = 8

    # eval_rounds = 500  # played against Random and Heuristic
    # eval_intervall = 5

    lr = 0.0002
    lr_stepsize = 30000000.0  # 300000
    lr_gamma = 0.3

    betas = (0.9, 0.999)
    gamma = 0.99  # discount factor

    K_epochs = 4  # 8  # update policy for K epochs
    eps_clip = 0.2  # clip parameter for PPO
    c1, c2 = 0.5, 0.005

    optimizer_weight_decay = 1e-5

    random_seed = None
