from Game import Game
from operator import add

def playTournament(players,rounds):
    scores = [0,0,0,0]
    for n in range(0,rounds):
        game = Game(players)
        lead = n%4
        game.mainGame(lead)
        scores = map(add,scores,game.rewards)
        print(scores)
