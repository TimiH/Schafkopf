from CardValues import SUITS

NONE = 0
TEAM = 1
WENZ = 2
SOLO = 3
#NoGame,3 Team games(Hearts Not allowed), Wenz, 4 Solo
MODES = [(NONE, NONE),
         (TEAM, SUITS['Eichel']), (TEAM, SUITS['Gras']), (TEAM, SUITS['Schellen']),
         (2, 0),
         (3, SUITS['Eichel']), (3, SUITS['Gras']), (3, SUITS['Herz']), (3, SUITS['Schellen'])]
