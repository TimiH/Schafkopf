from Game import Game
from Statistics import Statistics
from helper import rotateListBackwards, rotateListForward
from PlayerModels.ModelPlayer import ModelPlayer
from PlayerModels.PPO.LinearPolicy import LinearModel
from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer
from random import randint
from math import floor


# TODO implement fixed Seeds
def playFairTournament(players, rounds, laufendeBool=True, verbose=True):
    statistics = Statistics()
    statistics.setPlayerNames(players)
    for round in range(int(rounds)):
        gameFound = False
        while not gameFound:
            seed = randint(0, 1000000000)
            game = Game(players, 0, seed)
            game.setupGame()
            gameFound = game.playBidding()
        # print(f'(GameSeed:{game.seed})')
        for hand in range(4):
            if verbose:
                print(f'Playing: Round {round, hand}')
            rotatetedPlayers = rotateListForward(players, hand)
            game = Game(rotatetedPlayers, 0, seed=seed, laufendeBool=laufendeBool)
            game.setupGame()
            game.playBidding()
            game.continueGame()
            gameDict = game.getGameDict()
            statistics.updateSelf(gameDict, hand)
    if verbose:
        print('DONE')
    statistics.createDataFrame()
    return statistics


def playRandomTournament(players, rounds, verbose=False, laufendeBool=True):
    statistics = Statistics()
    statistics.setPlayerNames(players)
    for round in range(int(rounds) * 4):
        game = Game(players, round % 4, laufendeBool=laufendeBool)
        game.setupGame()
        gameFound = game.playBidding()
        if not gameFound:
            round -= 1
            continue
        if verbose:
            print(f'Playing: Round {round // 4, round % 4}')
        game.continueGame()
        gameDict = game.getGameDict()
        statistics.updateSelf(gameDict, 0)
    if verbose:
        print('DONE')
    statistics.createDataFrame()
    return statistics


# plays fair Tournament versus Heuristic and Random
def playEvalTournament(policy, rounds):
    p1, p3 = ModelPlayer('1', policy, eval=True), ModelPlayer('3', policy, eval=True)

    # heuristic
    p2, p4 = HeuristicPlayer('2'), HeuristicPlayer('4')
    statsHeuristc = playFairTournament([p1, p2, p3, p4], rounds, laufendeBool=False, verbose=False)
    evOverallHeu = statsHeuristc.getEVOverall().iloc[0, [0, 2]].mean()
    evPlayerHeu = statsHeuristc.getEVGameModePlayers().iloc[[0, 2],].mean()

    # random
    p2, p4 = RandomPlayer('2'), RandomPlayer('4')
    statsRandom = playFairTournament([p1, p2, p3, p4], rounds, laufendeBool=False, verbose=False)
    evOverallRan = statsRandom.getEVOverall().iloc[0, [0, 2]].mean()
    evPlayerRan = statsRandom.getEVGameModePlayers().iloc[[0, 2],].mean()

    return evOverallHeu, evPlayerHeu, evOverallRan, evPlayerRan
