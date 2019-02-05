from Deck import Deck
from Card import Card
from Player import Player
from Game import Game
from Bidding import Bidding
from Trick import Trick

p1 = Player("Tim")
p2 = Player("Paul")
p3 = Player("Robin.H")
p4 = Player("Chrissi")


players = [p1,p2,p3,p4]
game = Game(players)
game.mainGame()
print(game.history)
