from Deck import Deck
from Card import Card
from Player import Player
from Game import Game
from Bidding import Bidding
from Trick import Trick

p1 = Player("Tim")
p2 = Player("Paul")
p3 = Player("Robin.H")
p4 = Player("chrissi")


players = [p1,p2,p3,p4]
game = Game(players)
# print(getValidBidsForPlayer(p1))
game.mainGame()
print(game.gameMode)
print(game.offensivePlayers)
copy = game.copy()
t = Trick(1,0,copy)
t.playTrick()
print(t.history)
t.determineWinner()
print(t.winningPlayer)
print(t.score)
