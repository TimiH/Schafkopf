from Deck import Deck
from Card import Card
from Player import Player
from PlayerModels.RandomPlayer import RandomPlayer
from PlayerModels.MonteCarlo import MonteCarloPlayer

from Game import Game
from Bidding import Bidding
from Trick import Trick
from Tournament import playTournament
import time

p1 = MonteCarloPlayer("Tim")
p2 = RandomPlayer("Paul")
p3 = RandomPlayer("Robin.H")
p4 = RandomPlayer("Chrissi")

players = [p1,p2,p3,p4]
start = time.time()
playTournament(players,100)
end = time.time()
print("Time:", end-start)
