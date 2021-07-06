from Game import Game
import gym
from gym import spaces
from PlayerModels.RandomPlayer import RandomPlayer
import gym
from gym import error, spaces, utils
from gym.utils import seeding


class SchafkopfEnv(gym.Env):
    """Schafkopf environment for OpenAI gym"""
    metadata = {'render.modes': ['ansi']}

    def __init__(self, players, lead, seed=None):
        super(SchafkopfEnv, self).__innit__()
        self.action_space = spaces.MultiDiscrete(32)
        self.observation_space = spaces.dict()
        self.players = players
        self.game = Game(players, 0)
        self.game.setupGame()
        self.game.playBidding()
        if self.game.gameMode == (0, 0):
            self.reset()

    def step(self, action):
        pass

    def reset(self):
        self.game = Game(self.players, 0)
        self.game.setupGame()
        self.game.playBidding()
        self.game.continueTillNextAction()
        while self.game.gameMode == (0, 0):
            self.game = Game(self.players, 0)
            self.game.setupGame()
            self.game.playBidding()
            self.game.continueTillNextAction()

        return self.game.currentTrick.getNextValidAction()

    # starts new game
    def render(self, mode='human'):
        pass

    def seed(self, seed=None):
        pass

    def close(self):
        pass
