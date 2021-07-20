import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical
from PlayerModels.PPO.SETTINGS import Settings


class LinearModel(nn.Module):
    def __init__(self):
        super().__init__()
        # input 233
        self.hidden_neurons = 64
        self.inLayer = nn.Linear(217, self.hidden_neurons)
        self.midLayer = nn.Linear(self.hidden_neurons, self.hidden_neurons)
        self.actorLayer = nn.Linear(self.hidden_neurons, self.hidden_neurons)
        self.criticLayer = nn.Linear(self.hidden_neurons, self.hidden_neurons)
        self.actorOut = nn.Linear(self.hidden_neurons, 32)
        self.criticOut = nn.Linear(self.hidden_neurons, 1)
        self.double()

        self.device = Settings.device

    def forward(self, input):
        [inputVector, actionMask] = input

        x = F.relu(self.inLayer(inputVector))
        x = F.relu(self.midLayer(x))
        # Split into actor & critic
        ax = F.relu(self.actorLayer(x))
        ax = F.relu(self.actorOut(ax))
        cx = F.relu(self.criticLayer(x))
        cx = F.relu(self.criticOut(cx))

        ax = ax.masked_fill(actionMask == 0, -1e9)
        ax = F.softmax(ax, dim=-1)
        return ax, cx

    def evaluate(self, inputVector, action):
        actionLogProbabilities, stateValue = self(inputVector)
        dist = Categorical(actionLogProbabilities)

        actionLogProbabilities = dist.log_prob(action)
        distributionEntropy = dist.entropy()

        return actionLogProbabilities, torch.squeeze(stateValue), distributionEntropy

    def preprocess(self, stateVector):
        # input
        hand = np.array(list(stateVector['hand']))  # 32
        cardsPlayed = np.array(list(stateVector['cardsPlayed']))  # 32
        lead = np.array(list(stateVector['lead']))  # 4
        gameMode = np.array(list(stateVector['gameMode']))  # 7
        ranAway = np.array(list(stateVector['ranAway']))  # 1
        searched = np.array(list(stateVector['searched']))  # 1
        bidWinner = np.array(list(stateVector['bidWinner']))  # 4
        ownTeam = np.array(list(stateVector['ownTeam']))  # 4
        scores = np.true_divide(stateVector['scores'], 120)  # 4
        # ugly but unsure how np behaves here
        trickHistory = stateVector['trickHistoryPlayer']
        trickHistory = trickHistory[0] + trickHistory[1] + trickHistory[2] + trickHistory[3]
        trickHistory = np.array(list(trickHistory))  # 32*4
        test = [trickHistory, hand, cardsPlayed, lead, gameMode, ranAway, searched, bidWinner, ownTeam, scores]
        # for p in test:
        #     print(f'{p}{p.shape}')

        inputVector = np.concatenate(
            (trickHistory, hand, cardsPlayed, lead, gameMode, ranAway, searched, bidWinner, ownTeam, scores))

        # actionḾasking
        validCards = np.array(list(stateVector['validCards']))  # 32

        # return [torch.tensor(inputVector).float().to(self.device), torch.tensor(validCards).float().to(self.device)]
        return [torch.tensor(inputVector).to(self.device), torch.tensor(validCards).to(self.device)]
