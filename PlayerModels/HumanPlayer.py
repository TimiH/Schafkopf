from PlayerModels.Player import Player


class HumanPlayer(Player):
    def __init__(self, name, record=False, targetFile='', gui=False):
        self.name = name
        self.hand = []
        self.position = None
        self.record = record
        self.states = {}
        self.target = targetFile

    def makeBid(self, validBids):
