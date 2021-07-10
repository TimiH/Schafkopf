import pandas as pd
from helper import rotateListBackwards


# Statistics Module
# All scores are related to the order players get initialized
class Statistics:
    def __init__(self):
        self.gameCount = [0, 0, 0]  # Sauspiel, Wenz, Solo
        self.GamesWonCount = [0, 0, 0]
        self.BidByPlayer = [0, 0, 0, 0]  # Currently not interesting due to fixed bidding
        # [SauspielBid|Wenz|Solo|SauspielPartner|SauspielOPP|WenzOpp|SoloOpp]
        self.GamesPlayedByPlayer = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0]]
        self.GamesWonByPlayer = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0]]
        self.RewardsWonByPlayer = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0]]
        self.df = None
        self.rewardsOverall = [0, 0, 0, 0]
        self.dictionary = self.createDictionary()
        self.playerNames = []

    def updateSelf(self, gameDict, rotateBy):
        gameMode = gameDict['gameMode'][0]
        offensivePlayersWon = gameDict['offensivePlayersWon']

        # gameCount & GamesWon
        self.gameCount[gameMode - 1] += 1
        if offensivePlayersWon:
            self.GamesWonCount[gameMode - 1] += 1

        # BidByPlayer,GamesWonByPlayer
        self.updatePlayerStats(gameDict, rotateBy)

        # dict
        self.dictionary['gameMode'].append(gameMode)
        self.dictionary['gameValue'].append(gameDict['gameValue'])
        self.dictionary['leadingPlayer'].append(gameDict['leadingPlayer'])
        self.dictionary['schneider'].append(gameDict['schneider'])
        self.dictionary['schwarz'].append(gameDict['schwarz'])
        self.dictionary['seed'].append(gameDict['seed'])
        self.dictionary['laufende'].append(gameDict['laufende'])
        self.dictionary['offensivePlayersWon'].append(offensivePlayersWon)
        # Need Flipping
        scores = rotateListBackwards(gameDict['scores'], rotateBy)
        rewards = rotateListBackwards(gameDict['rewards'], rotateBy)
        self.rewardsOverall = list(map(lambda x, y: x + y, self.rewardsOverall, rewards))
        for n in range(4):
            keyRewards = 'rewards' + str(n)
            self.dictionary[keyRewards].append(rewards[n])
            keyScores = 'scores' + str(n)
            self.dictionary[keyScores].append(scores[n])

    def updatePlayerStats(self, gameDict, rotateBy):
        gameMode = gameDict['gameMode'][0]
        offensivePlayersWon = gameDict['offensivePlayersWon']
        offensivePlayersRotated = [(x - rotateBy) % 4 for x in gameDict['offensivePlayers']]
        rewardsPlayersWon = gameDict['rewards']
        rewardsPlayersWonRotated = rotateListBackwards(rewardsPlayersWon, rotateBy)
        # TODO
        # self.BidByPlayer[offensivePlayersRotated[0]] += 1

        # [SauspielBid|Wenz|Solo|SauspielPartner|SauspielOPP|WenzOpp|SoloOpp]
        # for readability: gamemode+4 for opposition, gameMode+3 for partner
        path = {
            1: 0,  # SauspielBid
            2: 1,  # Wenz
            3: 2,  # Solo
            4: 3,  # SauspielPartner
            5: 4,  # SauspielOPP
            6: 5,  # WenzOpp
            7: 6  # SoloOpp
        }
        for player in range(4):
            if gameMode == 1:
                bidWinner = offensivePlayersRotated[0]
                partner = offensivePlayersRotated[1]
                # BidTeam
                if player == bidWinner:
                    self.GamesPlayedByPlayer[player][path[gameMode]] += 1
                    self.RewardsWonByPlayer[player][path[gameMode]] += rewardsPlayersWonRotated[player]
                    if offensivePlayersWon:
                        self.GamesWonByPlayer[player][path[gameMode]] += 1
                elif player == partner:
                    self.GamesPlayedByPlayer[player][path[gameMode + 3]] += 1
                    self.RewardsWonByPlayer[player][path[gameMode + 3]] += rewardsPlayersWonRotated[player]
                    if offensivePlayersWon:
                        self.GamesWonByPlayer[player][path[gameMode + 3]] += 1
                else:
                    # Oppostion
                    self.GamesPlayedByPlayer[player][path[gameMode + 4]] += 1
                    self.RewardsWonByPlayer[player][path[gameMode + 4]] += rewardsPlayersWonRotated[player]
                    if not offensivePlayersWon:
                        self.GamesWonByPlayer[player][path[gameMode + 4]] += 1
            else:
                if player == offensivePlayersRotated[0]:
                    self.GamesPlayedByPlayer[player][path[gameMode]] += 1
                    self.RewardsWonByPlayer[player][path[gameMode]] += rewardsPlayersWonRotated[player]
                    if offensivePlayersWon:
                        self.GamesWonByPlayer[player][path[gameMode]] += 1
                else:
                    # Oppostion
                    self.GamesPlayedByPlayer[player][path[gameMode + 4]] += 1
                    self.RewardsWonByPlayer[player][path[gameMode + 4]] += rewardsPlayersWonRotated[player]
                    if not offensivePlayersWon:
                        self.GamesWonByPlayer[player][path[gameMode + 4]] += 1

    def createDictionary(self):
        dfDict = {
            'seed': [],
            'gameMode': [],
            'rewards0': [],
            'rewards1': [],
            'rewards2': [],
            'rewards3': [],
            'gameValue': [],
            'offensivePlayersWon': [],
            'leadingPlayer': [],
            'schneider': [],
            'schwarz': [],
            'laufende': [],
            'scores0': [],
            'scores1': [],
            'scores2': [],
            'scores3': [],
        }
        return dfDict

    def createDataFrame(self):
        df = pd.DataFrame(self.dictionary)
        self.df = df
        self.renameColumns()

    def setPlayerNames(self, playerList):
        for player in playerList:
            self.playerNames.append(player.name)

    def renameColumns(self):
        names = {
            'rewards0': self.playerNames[0],
            'rewards1': self.playerNames[1],
            'rewards2': self.playerNames[2],
            'rewards3': self.playerNames[3],
            'scores0': self.playerNames[0] + '_S',
            'scores1': self.playerNames[1] + '_S',
            'scores2': self.playerNames[2] + '_S',
            'scores3': self.playerNames[3] + '_S',
        }
        self.df.rename(columns=names, inplace=True)

    def getCumSum(self):
        df = self.df[self.playerNames]
        dfCumSums = df.cumsum()
        return dfCumSums

    def getCumSumRound(self):
        df = self.getCumSum()
        dfRound = df.iloc[::4, :]
        return dfRound

    def plotCumsums(self):
        df = self.getCumSum()
        ts = df.plot(grid=True, xlabel='Games', ylabel='Reward')
        return ts

    def plotCumSumsRound(self):
        df = self.getCumSumRound()
        tsRound = df.plot(grid=True, xlabel='Games', ylabel='Reward')
        return tsRound

    def getWinPercentagesOverall(self):
        winPercentages = list(map(lambda x, y: x / y, self.GamesWonCount, self.gameCount))
        names = ['Sauspiel', 'Wenz', 'Solo']
        cnames = dict(zip(range(3), names))
        df = pd.DataFrame(winPercentages).transpose()
        df = df.rename(columns=cnames)
        return df

    def getWinPercentagesPlayer(self):
        winPercentagesAll = []
        for player in range(4):
            winPercentages = list(
                map(lambda x, y: x / y, self.GamesWonByPlayer[player], self.GamesPlayedByPlayer[player]))
            winPercentagesAll.append(winPercentages)
        dfZip = dict(zip(self.playerNames, winPercentagesAll))
        df = pd.DataFrame(dfZip).transpose()
        names = ['SauspielBid', 'Wenz', 'Solo', 'SauspielPartner', 'SauspielOPP', 'WenzOpp', 'SoloOpp']
        cnames = dict(zip(range(7), names))
        df = df.rename(columns=cnames)
        return df

    def getEVOverall(self):
        totalGames = sum(self.gameCount)
        ev = [x / totalGames for x in self.rewardsOverall]
        df = pd.DataFrame(ev).transpose()
        cnames = dict(zip(range(4), self.playerNames))
        df = df.rename(columns=cnames)
        return df

    def getEVGameModePlayers(self):
        evAll = []
        for player in range(4):
            ev = list(map(lambda x, y: x / y, self.RewardsWonByPlayer[player], self.GamesWonByPlayer[player]))
            evAll.append(ev)
        dfZip = dict(zip(self.playerNames, evAll))
        df = pd.DataFrame(dfZip).transpose()
        names = ['SauspielBid', 'Wenz', 'Solo', 'SauspielPartner', 'SauspielOPP', 'WenzOpp', 'SoloOpp']
        cnames = dict(zip(range(7), names))
        df = df.rename(columns=cnames)
        return df
