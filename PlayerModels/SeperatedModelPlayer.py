from PlayerModels.Player import Player
from PlayerModels.PPO.Memory import Memory
from PlayerModels.staticBidding import choseTeamGame, choseWenzGameSimple, choseSoloGame
from StateVectorDict import createVectorDict
from torch.distributions import Categorical
import torch

from Card import Card
from CardValues import RANKS, REVERSEDSUITS


class SeperatedModelPlayer(Player):
    def __init__(self, name, policyTeam=None, policyWenz=None, policySolo=None, eval=True, record=False,
                 targetFile=None):
        self.name = name
        self.hand = []
        self.memory = Memory()
        self.policyTeam = policyTeam
        self.policyWenz = policyWenz
        self.policySolo = policySolo
        self.position = None
        self.eval = eval

        self.record = record
        self.states = {}
        self.target = targetFile

    def playCard(self, validCards, gameState, trickHistory):
        # encode state
        vectorDict = createVectorDict(self.hand, validCards, self.position, gameState, trickHistory)
        mode, _ = gameState['gameMode']
        if mode == 1:
            inputVector = self.policyTeam.preprocess(vectorDict)
            actionProbabilities, stateValue = self.policyTeam(inputVector)
        if mode == 2:
            inputVector = self.policyWenz.preprocess(vectorDict)
            actionProbabilities, stateValue = self.policyWenz(inputVector)
        if mode == 3:
            inputVector = self.policySolo.preprocess(vectorDict)
            actionProbabilities, stateValue = self.policySolo(inputVector)

        distribution = Categorical(actionProbabilities)
        # Playing
        if self.eval:
            action = torch.argmax(actionProbabilities, 0)
        # Training
        else:
            action = distribution.sample()
            # Memory stuff
            # input vector has len 2
            self.memory.states.append([i.detach() for i in inputVector])
            self.memory.actions.append(action)
            self.memory.logprobs.append(distribution.log_prob(action).detach())

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
        steps = 8
        # rewards = steps * [reward * 1.0]
        rewards = steps * [0.0]
        rewards[-1] = reward * 1.0
        self.memory.rewards += rewards

        # score = resultsDict['scores'][self.position]
        # scores = steps * [0.0]
        # scores[-1] = float(score)
        # self.memory.scores += scores

    def makeBid(self, validBids):
        teamGameChoice = choseTeamGame(validBids, self.hand)
        wenzGameChoice = choseWenzGameSimple(self.hand)
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
