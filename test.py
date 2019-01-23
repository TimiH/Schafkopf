from Deck import Deck
from Card import Card
from Player import Player
from Game import Game

p1 = Player("Tim")
p2 = Player("Paul")
p3 = Player("Robin.H")
p4 = Player("chrissi")


players = [p1,p2,p3,p4]
game = Game(players)
# game.setupGame()
# print(game.players)
#
# copy = game.copy()
# print(copy.players[0].hand)
game.mainGame()
print(game.bids)
