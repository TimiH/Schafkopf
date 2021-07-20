class Memory():
    def __init__(self):
        self.actions = []
        self.states = []
        self.logprobs = []
        self.rewards = []
        self.scores = []
        # self.teamScores = []
        self.done = []

    # needed to merge several memories into one for the PPO
    def update(self, memory):
        self.actions.extend(memory.actions)
        self.states.extend(memory.states)
        self.logprobs.extend(memory.logprobs)
        self.rewards.extend(memory.rewards)
        self.done.extend(memory.done)

    def updateReward(self, reward, score):
        self.rewards.append(reward)
        self.scores.append(score)
        # self.teamScores.append(teamScore)

    def reset(self):
        self.actions = []
        self.states = []
        self.logprobs = []
        self.rewards = []
        self.scores = []
        # self.teamScores = []
        self.done = []
