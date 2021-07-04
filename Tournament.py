from Game import Game
from Statistics import Statistics
from helper import recreateHandsfromHistory, rotateListBackwards, rotateListForward
from random import randint
from math import floor


# TODO implement fixed Seeds
def playFairTournament(players, rounds, laufendeBool=True):
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
            game = Game(rotatetedPlayers, 0, seed=seed, laufendeBool=laufendeBool)
            game.setupGame()
            game.playBidding()
            game.continueGame()
            gameDict = game.getGameDict()
            statistics.updateSelf(gameDict, hand)
    print('DONE')
    statistics.createDataFrame()
    return statistics


def playRandomTournament(players, rounds, laufendeBool=True):
    statistics = Statistics()
    statistics.setPlayerNames(players)
    for round in range(rounds * 4):
        game = Game(players, round % 4, laufendeBool=laufendeBool)
        game.setupGame()
        gameFound = game.playBidding()
        if not gameFound:
            round -= 1
            continue
        print(f'Playing: Round {floor(round / 4), round % 4}')
        game.continueGame()
        gameDict = game.getGameDict()
        statistics.updateSelf(gameDict, 0)
    print('DONE')
    statistics.createDataFrame()
    return statistics
