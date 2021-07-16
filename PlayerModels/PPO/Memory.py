class Memory():
    def __init__(self):
        self.actions = []
        self.states = []
        self.logprobs = []
        self.rewards = []
        self.scores = []
        # self.teamScores = []
        self.done = []

    def update(self, action, state, logprobs, reward, done):
        self.actions.extend(action)
        self.states.extend(state)
        self.logprobs.extend(logprobs)
        self.rewards.extend(reward)
        self.done.extend(done)

    def updateReward(self, reward, score):
        self.rewards.append(reward)
        self.scores.append(score)
        # self.teamScores.append(teamScore)

    def reset(self):
        self.actions = []
        self.states = []
        self.logprobs = []
        self.rewards = []
        self.done = []
