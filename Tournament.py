
from Game import Game
from operator import add
from helper import recreateHandsfromHistory, sortHand
from copy import deepcopy
from random import randint

# rotates Players forward by 1 Position [0,1,2,3]->[1,2,3,0]
def rotatePlayersForward(players, n):
    return players[n:] + players[:n]


# rotates Players by backwards 1 Position [1,2,3,0]->[0,1,2,3], used for score manipulation
def rotatePlayersBackwards(players, n):
    return players[-n:] + players[:-n]


# TODO implement fixed Seeds
def playFairTournament(players, rounds):
    scores = [0, 0, 0, 0]
    # TODO implenment games played to once different agents exist
    # playedGames = [0, 0, 0, 0]
    for i in range(rounds):
        game = Game(players, 0, seed=randint(0, 1000000000))
        for n in range(4):
            gamecopy = deepcopy(game)
            gamecopy.players = rotatePlayersForward(gamecopy.players, n)
            gamecopy.mainGame()
            print("Round: " + str(i) + '.' + str(n))
            # print(*players, sep=',')
            print('Rewards', gamecopy.rewards)
            scores = list(map(add, scores, rotatePlayersBackwards(gamecopy.rewards, n)))
        print('Scores after Round', scores)
    print('Scores after Tournament', scores)


def playTournament(players, rounds):
    scores = [0, 0, 0, 0]
    playedGames = [0, 0, 0, 0]

    for n in range(0, rounds):
        print("-------------------\nRound:{}".format(n))
        lead = n % 4
        game = Game(players, lead)  # 100
        game.mainGame()
        offensivePlayer = game.offensivePlayers[0]
        playedGames[offensivePlayer] += 1
        # print(game.rewards,game.offensivePlayers,game.offenceWon())
        # if game.offenceWon():
        #     hands = recreateHandsfromHistory(game.history)
        #     print(game.bids,"Leading Player",game.leadingPlayer,"offensive",game.offensivePlayers)
        #     print(hands)
        #     print(game.scores)
        #     print(game.history)
        #     print(game.rewards)
        #     break
        hands = recreateHandsfromHistory(game.history)
        # for hand in hands:
        #     hand = sortHand(hand)
        #     print(hand)
        print(game.bids, "Leading Player", game.leadingPlayer, "offensive", game.offensivePlayers)
        print(game.scores)
        print(game.history)
        print(game.rewards)
        scores = list(map(add, scores, game.rewards))
    print(scores)
    print(playedGames)
