from torch.utils import data
import torch


# used for loading the PPO update
class Dataset(data.Dataset):
    def __init__(self, states, actions, logprobs, rewards):
        self.states = states
        self.actions = actions
        self.logprobs = logprobs
        self.rewards = rewards

    def __len__(self):
        return len(self.actions)

    def __getitem__(self, index):
        return [self.states[index], self.actions[index], self.logprobs[index], self.rewards[index]]

    def custom_collate(self, batch):
        states_batch, actions_batch, logprobs_batch, rewards_batch = zip(*batch)

        # states = [state[0] for state in states_batch]
        # states = torch.stack(states).detach()

        states = []
        transposed_states = list(map(list, zip(*states_batch)))
        states.append(torch.stack(transposed_states[0]).detach())
        states.append(torch.stack(transposed_states[1]).detach())

        actions = torch.stack(actions_batch).detach()
        logprobs = torch.stack(logprobs_batch).detach()
        rewards = torch.tensor(rewards_batch)

        return [states, actions, logprobs, rewards]
