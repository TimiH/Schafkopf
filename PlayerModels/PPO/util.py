import torch
from PlayerModels.PPO.LinearPolicy import LinearModel
from PlayerModels.PPO.TeamPolicy import TeamModel
from PlayerModels.PPO.WenzPolicy import WenzModel
from PlayerModels.PPO.SoloPolicy import SoloModel
from PlayerModels.ModelPlayer import ModelPlayer
from PlayerModels.SeperatedModelPlayer import SeperatedModelPlayer
import os


def loadLinear(experiment, episode):
    path = os.getcwd() + "/PlayerModels/PPO/experiments/checkpoints/" + str(experiment) + '/' + str(episode) + '.pt'
    policy = LinearModel()
    policy.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    return policy


def loadTeam(experiment, episode):
    path = os.getcwd() + "/PlayerModels/PPO/experiments/checkpoints/" + str(experiment) + '/team/' + str(
        episode) + '.pt'
    policy = TeamModel()
    policy.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    return policy


def loadWenz(experiment, episode):
    path = os.getcwd() + "/PlayerModels/PPO/experiments/checkpoints/" + str(experiment) + '/wenz/' + str(
        episode) + '.pt'
    policy = WenzModel()
    policy.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    return policy


def loadSolo(experiment, episode):
    path = os.getcwd() + "/PlayerModels/PPO/experiments/checkpoints/" + str(experiment) + '/solo/' + str(
        episode) + '.pt'
    policy = SoloModel()
    policy.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    return policy


def loadSeperatedPlayer(name, experiment, episode):
    policyT = loadTeam(experiment, episode)
    policyW = loadWenz(experiment, episode)
    policyS = loadSolo(experiment, episode)
    player = SeperatedModelPlayer(str(name), policyTeam=policyT, policySolo=policyS, policyWenz=policyW,eval=True)
    return player


def loadLinearPlayer(name, experiment, episode):
    policy = loadLinear(experiment, episode)
    player = ModelPlayer(str(name), policy,eval=True,debug=False)
    return player
