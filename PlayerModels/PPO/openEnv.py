from Game import Game
import gym
from gym import spaces
from PlayerModels.RandomPlayer import RandomPlayer


class SchafkopfEnv(gym.Env):
    """Schafkopf environment for OpenAI gym"""
    metadata = {'render.modes': ['human']}

    def __init__(self, players, lead, seed=None):
        super.(SchafkopfEnv, self).__innit__()
        self.players = players
        self.game = Game(players, 0)
        self.game.setupGame()
        self.game.playBidding()
        if self.game.gameMode == (0, 0)
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
