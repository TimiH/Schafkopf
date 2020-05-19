from Game import Game
from operator import add
from helper import recreateHandsfromHistory, sortHand


def playTournament(players, rounds):
    scores = [0, 0, 0, 0]
    playedGames = [0, 0, 0, 0]

    for n in range(0, rounds):
        lead = n % 4
        game = Game(players, lead, 100)  # 100
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
        scores = map(add, scores, game.rewards)
    print(scores)
    print(playedGames)
