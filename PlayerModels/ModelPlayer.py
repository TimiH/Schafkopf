from PlayerModels.Player import Player
from PlayerModels.PPO.Memory import Memory
from PlayerModels.staticBidding import choseTeamGame, choseWenzGameRevised, choseSoloGame
from StateVectorDict import createVectorDict
from torch.distributions import Categorical
import torch

from Card import Card
from CardValues import RANKS, REVERSEDSUITS


class ModelPlayer(Player):
    def __init__(self, name, policy, eval=True, record=False, targetFile=None):
        self.name = name
        self.hand = []
        self.memory = Memory()
        self.policy = policy
        self.position = None
        self.eval = eval

        self.record = record
        self.states = {}
        self.target = targetFile

    def playCard(self, validCards, gameState, trickHistory):
        # encode state
        vectorDict = createVectorDict(self.hand, validCards, self.position, gameState, trickHistory)
        inputVector = self.policy.preprocess(vectorDict)
        actionProbabilities, stateValue = self.policy(inputVector)
        distribution = Categorical(actionProbabilities)
        # Playing
        if self.eval:
            action = torch.argmax(actionProbabilities, 0)
        # Training
        else:
            action = distribution.sample
            # Memory stuff
            self.memory.states.append([i.detatch() for i in inputVector])
            self.memory.actions.append(action)
            self.memory.logprobs.append(actionProbabilities)

        # convert action to card
        index = action.item()
        suit, rank = index // 8, index % 8
        card = Card(REVERSEDSUITS[suit], RANKS[rank])
        if card not in validCards:
            raise Exception
        else:
            return card

    def setResults(self, resultsDict):
        done = 7 * [False]
        done.append(True)
        self.memory.done += done

        reward = resultsDict['rewards'][self.position]
        steps = len(self.memory)
        rewards = steps * [0.0]
        rewards[-1] = reward
        self.memory.rewards += rewards

        score = resultsDict['scores'][self.position]
        scores = steps * [0.0]
        scores[-1] = score
        self.memory.scores += scores

    def makeBid(self, validBids):
        teamGameChoice = choseTeamGame(validBids, self.hand)
        wenzGameChoice = choseWenzGameRevised(self.hand)
        soloGameChoice = choseSoloGame(validBids, self.hand)
        bids = []

        max = (0, 0)
        if teamGameChoice[0] > max[0]:
            max = teamGameChoice
        if wenzGameChoice[0] > max[0]:
            max = wenzGameChoice
        if soloGameChoice[0] > max[0]:
            max = soloGameChoice
        return max
