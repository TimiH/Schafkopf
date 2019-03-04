from Player import Player

class MCTS(object):
    __init__(self, gamestate,validCards,hand,position):
        self.gamestate = gamestate
        self.history = gamestate.history
        self.playerPosition = position


class TreeNode(object):
    __init__(self,gamestate,card,available cards,simRuns=100,simTime=2):
        self.stats = [0,0]
        self.gamestate = gamestate.currentTrick.histoy.append(Card)
        self.players = []
        for n in range(4):
            p = Player("MCTS "+n)
