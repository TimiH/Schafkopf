from Game import Game
from PlayerModels.HeuristicPlayer import HeuristicPlayer
from PlayerModels.staticBidding import getCardsOfSuit
from CardValues import REVERSEDSUITS
from GuiTools.renderGame import renderGameState
import pickle
players = [HeuristicPlayer(str(i)) for i in range(4)]
test = False
while not test:
    #test=True
    g = Game(players,0)
    g.setupGame()
    g.playBidding()
    if g.gameMode != (0,0) and g.offensivePlayers == [3] and g.gameMode[0] == 3:
        gamemode = g.gameMode
        g.continueTillNextAction()
        # g.currentTrick.nextAction()
        # g.currentTrick.nextAction()
        # g.currentTrick.nextAction()
        print(g.playersHands)
        print(g.currentTrick.history)
        test = True


    # g.continueTillNextAction()
    # g.currentTrick.history.append(g.playersHands[0][0])
    # g.currentTrick.nextAction()
    # g.currentTrick.nextAction()
    # state = g.getGameDict()
    # hist = g.currentTrick.history
    # img = renderGameState(state, hist)
    # img.show()
    # with open('/home/tim/Work/Schafkopf/Evaluation/testCases/4teamAH.st', 'wb') as out:
    #     pickle.dump(state, out, pickle.HIGHEST_PROTOCOL)