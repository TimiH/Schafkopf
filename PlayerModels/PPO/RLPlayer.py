from PlayerModels.Player import Player
from PlayerModels.PPO.Memory import Memory

class RlPlayer(Player):
    def __init__(self, name, record=False, targetFile=''):
        self.name = name
        self.hand = []
        self.position = None
        self.record = record
        self.states = {}
        self.target = targetFile