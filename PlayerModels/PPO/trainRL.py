from tensorboard import program
from PlayerModels.PPO.LinearPolicy import LinearModel
from PlayerModels.PPO.SETTINGS import Settings
from PlayerModels.PPO.PPO import PPO
from PlayerModels.ModelPlayer import ModelPlayer
from PlayerModels.PPO.Memory import Memory
from Tournament import playFairTournament, playRandomTournament, playEvalTournament

import torch
import glob
import re
import os
import pickle


def main():
    # init Tensorboard

    # tb = program.TensorBoard()
    # tb.configure(argv=[None, '--logdir', Settings.runFolder])
    # tb.launch()

    # Policy new or newest version
    policy = LinearModel()
    policy.to(Settings.device)
    episodes = generation = 0
    path = '/PlayerModels/PPO/checkpoints/'
    checkpoints = glob.glob(os.getcwd() + '/PlayerModels/PPO/checkpoints/*.pt')
    if checkpoints:
        latest = max(checkpoints, key=lambda x: int(re.findall(r'\d+', x)[0]))
        print(f'Loading Policy checkpoint {latest}')
        policy.load_state_dict(torch.load(latest))
        generation = len(checkpoints)
        episodes = generation

    ppo = PPO(policy, [Settings.lr, Settings.lr_stepsize, Settings.lr_gamma], Settings.betas, Settings.gamma,
              Settings.K_epochs, Settings.eps_clip, Settings.batch_size, Settings.mini_batch_size, c1=Settings.c1,
              c2=Settings.c2, start_episode=generation - 1)

    # players
    players = [ModelPlayer(str(i), policy, eval=False) for i in range(4)]

    # generate Games and update
    for _ in range(Settings.episodes):
        Settings.logger.info("---------------------")
        Settings.logger.info("playing " + str(Settings.update_games) + " games")
        # play games
        # stats = playFairTournament(players, Settings.update_games / 4, verbose=False, laufendeBool=False)
        stats = playRandomTournament(players, Settings.update_games / 4, laufendeBool=False)
        Settings.logger.info("Games played")

        # safe stats to pickle
        # Settings.logger.info("Saving stats")
        # name = '/PlayerModels/PPO/trainingStats/' + str(episodes) + '.p'
        # with open(os.getcwd() + name, 'wb') as out:
        #     pickle.dump(stats, out, pickle.HIGHEST_PROTOCOL)
        # Settings.logger.info("Stats saved")

        # update the policy
        Settings.logger.info("updating policy")

        overallMemory = Memory()
        for p in players:
            overallMemory.update(p.memory)
            del p.memory
        Settings.logger.info("Memory created")

        ppo.update(overallMemory, episodes)

        # Reseting players
        players = [ModelPlayer(str(i), ppo.policy_old, eval=False) for i in range(4)]

        # saving Policy
        episodes += 1
        torch.save(ppo.policy_old.state_dict(), Settings.checkFolder + str(episodes) + ".pt")
        Settings.logger.info(f"Weights Saved! Episode: {episodes} completed")

        # running eval
        Settings.logger.info(f"Running Eval: 2x {Settings.eval_rounds}")
        evOverallHeu, evPlayerHeu, evOverallRan, evPlayerRan = playEvalTournament(ppo.policy_old, Settings.eval_rounds)
        evPlayerHeu = list(evPlayerHeu.iteritems())
        evPlayerRan = list(evPlayerRan.iteritems())

        # Logging
        Settings.logger.info("Logging EVs")
        Settings.logger.infor(f'EV Heuristic: {evPlayerHeu}')
        Settings.logger.infor(f'EV Random: {evPlayerRan}')
        Settings.summary_writer.add_scalar('EV/Heuristic/Overall', evOverallHeu, episodes)
        Settings.summary_writer.add_scalar('EV/Random/Overall', evOverallHeu, episodes)
        for i in evPlayerHeu:
            Settings.summary_writer.add_scalar('EV/Heuristic/' + i[0], i[1], episodes)
        for i in evPlayerRan:
            Settings.summary_writer.add_scalar('EV/Random/' + i[0], i[1], episodes)


if __name__ == '__main__':
    main()
