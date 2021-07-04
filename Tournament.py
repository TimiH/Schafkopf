from Game import Game
from operator import add
from Statistics import Statistics
from helper import recreateHandsfromHistory, rotateListBackwards, rotateListForward
from copy import deepcopy
from random import randint
import pandas as pd


# TODO implement fixed Seeds
def playFairTournament(players, rounds):
    statistics = Statistics()
    statistics.setPlayerNames(players)
    for round in range(rounds):
        gameFound = False
        while not gameFound:
            seed = randint(0, 1000000000)
            game = Game(players, 0, seed)
            game.setupGame()
            gameFound = game.playBidding()
        # print(f'(GameSeed:{game.seed})')
        for hand in range(4):
            print(f'Playing: Round {round, hand}')
            rotatetedPlayers = rotateListForward(players, hand)
            game = Game(rotatetedPlayers, 0, seed)
            game.setupGame()
            game.playBidding()
            game.continueGame()
            gameDict = game.getGameDict()
            statistics.updateSelf(gameDict, hand)
    print('DONE')
    statistics.createDataFrame()
    return statistics
