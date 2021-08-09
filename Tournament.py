from Game import Game
from Statistics import Statistics
from helper import rotateListBackwards, rotateListForward
from PlayerModels.ModelPlayer import ModelPlayer
from PlayerModels.SeperatedModelPlayer import SeperatedModelPlayer
from PlayerModels.PPO.LinearPolicy import LinearModel
from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.HeuristicPlayer import HeuristicPlayer
from PlayerModels.GreedyPlayer import GreedyPlayer
from random import randint

from math import floor


# TODO implement fixed Seeds
def playFairTournament(players, rounds, mode=0, laufendeBool=True, verbose=True):
    statistics = Statistics()
    statistics.setPlayerNames(players)
    for round in range(int(rounds)):
        gameFound = False
        while not gameFound:
            seed = randint(0, 1000000000)
            game = Game(players, 0, seed)
            game.setupGame()
            gameFound = game.playBidding()
            if mode != 0 and game.gameMode[0] != mode:
                gameFound = False
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


def playRandomTournament(players, rounds, mode=0, verbose=False, laufendeBool=True):
    statistics = Statistics()
    statistics.setPlayerNames(players)
    for round in range(int(rounds) * 4):
        gameFound = False
        while not gameFound:
            game = Game(players, round % 4)
            game.setupGame()
            gameFound = game.playBidding()
            if mode != 0 and game.gameMode[0] != mode:
                gameFound = False
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
def playEvalTournament(policy, rounds, mode=0):
    p1, p3 = ModelPlayer('1', policy, eval=True, debug=False), ModelPlayer('3', policy, eval=True, debug=False)

    # heuristic
    p2, p4 = HeuristicPlayer('2'), HeuristicPlayer('4')
    statsHeuristc = playFairTournament([p1, p2, p3, p4], rounds, mode=mode, laufendeBool=False, verbose=False)
    evOverallHeu = statsHeuristc.getEVOverall().iloc[0, [0, 2]].mean()
    evPlayerHeu = statsHeuristc.getEVGameModePlayers().iloc[[0, 2],].mean()
    evOverallPerHeu = statsHeuristc.getWinPentagesTotalPlayer().iloc[0, [0, 2]].mean()
    evPlayerPerHeu = statsHeuristc.getWinPercentagesPlayer().iloc[[0, 2],].mean()

    # random
    p2, p4 = RandomPlayer('2'), RandomPlayer('4')
    statsRandom = playFairTournament([p1, p2, p3, p4], rounds, mode=mode, laufendeBool=False, verbose=False)
    evOverallRan = statsRandom.getEVOverall().iloc[0, [0, 2]].mean()
    evPlayerRan = statsRandom.getEVGameModePlayers().iloc[[0, 2],].mean()
    evOverallPerRan = statsRandom.getWinPentagesTotalPlayer().iloc[0, [0, 2]].mean()
    evPlayerPerRan = statsRandom.getWinPercentagesPlayer().iloc[[0, 2],].mean()

    # greedy
    p2, p4 = GreedyPlayer('2'), GreedyPlayer('4')
    statsGreedy = playFairTournament([p1, p2, p3, p4], rounds, mode=mode, laufendeBool=False, verbose=False)
    evOverallGre = statsGreedy.getEVOverall().iloc[0, [0, 2]].mean()
    evPlayerGre = statsGreedy.getEVGameModePlayers().iloc[[0, 2],].mean()
    evOverallPerGre = statsGreedy.getWinPentagesTotalPlayer().iloc[0, [0, 2]].mean()
    evPlayerPerGre = statsGreedy.getWinPercentagesPlayer().iloc[[0, 2],].mean()
    statsDict = {
        'evOverallHeu': evOverallHeu,
        'evPlayerHeu': evPlayerHeu,
        'evOverallPerHeu': evOverallPerHeu,
        'evPlayerPerHeu': evPlayerPerHeu,
        'evOverallRan': evOverallRan,
        'evPlayerRan': evPlayerRan,
        'evOverallPerRan': evOverallPerRan,
        'evPlayerPerRan': evPlayerPerRan,
        'evOverallGre': evOverallGre,
        'evPlayerGre': evPlayerGre,
        'evOverallPerGre': evOverallPerGre,
        'evPlayerPerGre': evPlayerPerGre
    }
    return statsDict


def playEvalTournamentSeperated(policy, rounds, mode=0):
    if mode == 1:
        p1 = SeperatedModelPlayer('1', policyTeam=policy, eval=False)
        p3 = SeperatedModelPlayer('2', policyTeam=policy, eval=False)
    if mode == 2:
        p1 = SeperatedModelPlayer('1', policyWenz=policy, eval=False)
        p3 = SeperatedModelPlayer('2', policyWenz=policy, eval=False)
    if mode == 3:
        p1 = SeperatedModelPlayer('1', policySolo=policy, eval=False)
        p3 = SeperatedModelPlayer('2', policySolo=policy, eval=False)

    # heuristic
    p2, p4 = HeuristicPlayer('2'), HeuristicPlayer('4')
    statsHeuristc = playFairTournament([p1, p2, p3, p4], rounds, mode=mode, laufendeBool=False, verbose=False)
    evOverallHeu = statsHeuristc.getEVOverall().iloc[0, [0, 2]].mean()
    evPlayerHeu = statsHeuristc.getEVGameModePlayers().iloc[[0, 2],].mean()
    evOverallPerHeu = statsHeuristc.getWinPentagesTotalPlayer().iloc[0, [0, 2]].mean()
    evPlayerPerHeu = statsHeuristc.getWinPercentagesPlayer().iloc[[0, 2],].mean()

    # random
    p2, p4 = RandomPlayer('2'), RandomPlayer('4')
    statsRandom = playFairTournament([p1, p2, p3, p4], rounds, mode=mode, laufendeBool=False, verbose=False)
    evOverallRan = statsRandom.getEVOverall().iloc[0, [0, 2]].mean()
    evPlayerRan = statsRandom.getEVGameModePlayers().iloc[[0, 2],].mean()
    evOverallPerRan = statsRandom.getWinPentagesTotalPlayer().iloc[0, [0, 2]].mean()
    evPlayerPerRan = statsRandom.getWinPercentagesPlayer().iloc[[0, 2],].mean()

    statsDict = {
        'evOverallHeu': evOverallHeu,
        'evPlayerHeu': evPlayerHeu,
        'evOverallPerHeu': evOverallPerHeu,
        'evPlayerPerHeu': evPlayerPerHeu,
        'evOverallRan': evOverallRan,
        'evPlayerRan': evPlayerRan,
        'evOverallPerRan': evOverallPerRan,
        'evPlayerPerRan': evPlayerPerRan
    }
    return statsDict


def playBaseLineTournament(players, rounds, mode=0):
    p1, p3 = players[0], players[1]
    # heuristic
    p2, p4 = HeuristicPlayer('2'), HeuristicPlayer('4')
    print('Heuristic')
    statsHeuristc = playFairTournament([p1, p2, p3, p4], rounds, mode=mode, laufendeBool=False, verbose=False)
    evOverallHeu = statsHeuristc.getEVOverall().iloc[0, [0, 2]].mean()
    evPlayerHeu = statsHeuristc.getEVGameModePlayers().iloc[[0, 2],].mean()
    evOverallPerHeu = statsHeuristc.getWinPentagesTotalPlayer().iloc[0, [0, 2]].mean()
    evPlayerPerHeu = statsHeuristc.getWinPercentagesPlayer().iloc[[0, 2],].mean()

    # random
    print('Random')

    p2, p4 = RandomPlayer('2'), RandomPlayer('4')
    statsRandom = playFairTournament([p1, p2, p3, p4], rounds, mode=mode, laufendeBool=False, verbose=False)
    evOverallRan = statsRandom.getEVOverall().iloc[0, [0, 2]].mean()
    evPlayerRan = statsRandom.getEVGameModePlayers().iloc[[0, 2],].mean()
    evOverallPerRan = statsRandom.getWinPentagesTotalPlayer().iloc[0, [0, 2]].mean()
    evPlayerPerRan = statsRandom.getWinPercentagesPlayer().iloc[[0, 2],].mean()

    # greedy
    print('Greedy')

    p2, p4 = GreedyPlayer('2'), GreedyPlayer('4')
    statsGreedy = playFairTournament([p1, p2, p3, p4], rounds, mode=mode, laufendeBool=False, verbose=False)
    evOverallGre = statsGreedy.getEVOverall().iloc[0, [0, 2]].mean()
    evPlayerGre = statsGreedy.getEVGameModePlayers().iloc[[0, 2],].mean()
    evOverallPerGre = statsGreedy.getWinPentagesTotalPlayer().iloc[0, [0, 2]].mean()
    evPlayerPerGre = statsGreedy.getWinPercentagesPlayer().iloc[[0, 2],].mean()
    statsDict = {
        'evOverallHeu': evOverallHeu,
        'evPlayerHeu': evPlayerHeu,
        'evOverallPerHeu': evOverallPerHeu,
        'evPlayerPerHeu': evPlayerPerHeu,
        'evOverallRan': evOverallRan,
        'evPlayerRan': evPlayerRan,
        'evOverallPerRan': evOverallPerRan,
        'evPlayerPerRan': evPlayerPerRan,
        'evOverallGre': evOverallGre,
        'evPlayerGre': evPlayerGre,
        'evOverallPerGre': evOverallPerGre,
        'evPlayerPerGre': evPlayerPerGre
    }
    return statsDict
