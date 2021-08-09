from Game import Game
from Card import Card
from CardValues import REVERSEDSUITS
from PlayerModels.HeuristicPlayer import HeuristicPlayer
import pickle
import glob
import os
from PlayerModels.PPO.util import loadSeperatedPlayer


def collectStates():
    path = os.getcwd() + "/Evaluation/testCases/"
    globs = glob.glob(path + '*.st')
    globs.sort()
    states = []
    for g in globs:
        statefile = open(g, 'rb')
        state = pickle.load(statefile)
        states.append(state)
    return states


def runTest(player, states):
    # Team
    t1 = testCaseRanaway(player, states[0], 0, False)
    t2 = testCaseRanaway(player, states[1], 0, True)
    t3 = testCaseSearched(player, states[2], 0)
    # TeamCard
    t4, _ = testCaseCard(player, states[3], 0, 2, 'A')  # AH
    t5, _ = testCaseCard(player, states[4], 0, 0, 'O')  # OE fix OH
    # Wenz
    t6, _ = testCaseCard(player, states[5], 0, 0, 'U')  # UE
    t7, _ = testCaseCard(player, states[6], 3, 0, '8')  # 8E
    t8, _ = testCaseCard(player, states[7], 2, 2, 'A')  # AH
    # Solo
    t9, _ = testCaseCard(player, states[8], 2, 2, 'A')  # AH remove KS
    t10, _ = testCaseCard(player, states[9], 3, 0, '9')  # 9E

    result = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]
    return result


def testCaseCard(player, gamedict, pos, suit, rank):
    players = [HeuristicPlayer(str(i)) for i in range(4)]
    players[pos] = player
    g = Game(players, 0, gameDict=gamedict)
    g.continueTillNextAction()
    g.currentTrick.nextAction()

    card = Card(REVERSEDSUITS[suit], rank)
    if card not in g.currentTrick.history:
        test = False
    else:
        test = True
    return test, g.currentTrick.history


def testCaseRanaway(player, gamedict, pos, flip):
    players = [HeuristicPlayer(str(i)) for i in range(4)]
    players[pos] = player
    g = Game(players, 0, gameDict=gamedict)
    g.continueTillNextAction()
    g.currentTrick.playTrick()
    g.continueTillNextAction()
    if flip:
        return not g.ranAway
    else:
        return g.ranAway


def testCaseSearched(player, gamedict, pos):
    players = [HeuristicPlayer(str(i)) for i in range(4)]
    players[pos] = player
    g = Game(players, 0, gameDict=gamedict)
    g.continueTillNextAction()
    g.currentTrick.playTrick()
    g.continueTillNextAction()
    return g.searched


states = collectStates()
p1 = loadSeperatedPlayer('Sep1', 132, 500)

results = runTest(p1, states)
