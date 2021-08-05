from tensorboard import program
from PlayerModels.PPO.TeamPolicy import TeamModel
from PlayerModels.PPO.WenzPolicy import WenzModel
from PlayerModels.PPO.SoloPolicy import SoloModel
from PlayerModels.PPO.SETTINGS import Settings
from PlayerModels.PPO.PPO import PPO
from PlayerModels.SeperatedModelPlayer import SeperatedModelPlayer
from PlayerModels.PPO.Memory import Memory
from Tournament import playFairTournament, playRandomTournament, playEvalTournament

import torch
import glob
import re
import os
import pickle


def main(tSettings, mode):
    # Policy new or newest version
    if mode == 1:
        policy = TeamModel()
    if mode == 2:
        policy = WenzModel()
    if mode == 3:
        policy = SoloModel()

    policy.to(Settings.device)
    episodes = generation = 0
    # path = '/PlayerModels/PPO/checkpoints/'
    # checkpoints = glob.glob(os.getcwd() + '/PlayerModels/PPO/checkpoints/*.pt')
    checkpoints = glob.glob(tSettings.checkpoints + '*.pt')

    if checkpoints:
        latest = max(checkpoints, key=os.path.getctime)
        print(f'Loading Policy checkpoint {latest}')
        policy.load_state_dict(torch.load(latest))
        generation = len(checkpoints)
        episodes = generation

    ppo = PPO(policy, [Settings.lr, tSettings.lr_stepsize, Settings.lr_gamma], Settings.betas, Settings.gamma,
              tSettings.K_epochs, Settings.eps_clip, tSettings.batch_size, tSettings.mini_batch_size, c1=Settings.c1,
              c2=Settings.c2, start_episode=generation - 1, sumWriter=tSettings.summary_writer)

    # players
    if mode == 1:
        players = [SeperatedModelPlayer(str(i), policyTeam=ppo.policy_old, eval=False) for i in range(4)]
    if mode == 2:
        players = [SeperatedModelPlayer(str(i), policyWenz=ppo.policy_old, eval=False) for i in range(4)]
    if mode == 3:
        players = [SeperatedModelPlayer(str(i), policySolo=ppo.policy_old, eval=False) for i in range(4)]

    # generate Games and update
    for _ in range(tSettings.episodes):
        Settings.logger.info("---------------------")
        Settings.logger.info("playing " + str(tSettings.update_games) + " games")
        # play games
        stats = playRandomTournament(players, tSettings.update_games / 4, mode=mode, laufendeBool=False)
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
        ppo.lr_scheduler.step(episodes)

        # Reseting players
        if mode == 1:
            players = [SeperatedModelPlayer(str(i), policyTeam=policy, eval=False) for i in range(4)]
        if mode == 2:
            players = [SeperatedModelPlayer(str(i), policyWenz=policy, eval=False) for i in range(4)]
        if mode == 3:
            players = [SeperatedModelPlayer(str(i), policySolo=policy, eval=False) for i in range(4)]

        # saving Policy
        episodes += 1
        torch.save(ppo.policy_old.state_dict(), tSettings.checkpoints + str(episodes) + ".pt")
        Settings.logger.info(f"Weights Saved! Episode: {episodes} completed")

        # running eval
        if episodes % tSettings.eval_interval == 0:
            Settings.logger.info(f"Running Eval: 2x {tSettings.eval_rounds}")

            statsDict = playEvalTournament(ppo.policy_old, tSettings.eval_rounds, mode=mode)
            # assinging
            evPlayerHeu = list(statsDict['evPlayerHeu'].iteritems())
            evPlayerRan = list(statsDict['evPlayerRan'].iteritems())
            evPlayerPerHeu = list(statsDict['evPlayerPerHeu'].iteritems())
            evPlayerPerRan = list(statsDict['evPlayerPerRan'].iteritems())

            evOverallHeu = statsDict['evOverallHeu']
            evOverallRan = statsDict['evOverallRan']
            evOverallPerHeu = statsDict['evOverallPerHeu']
            evOverallPerRan = statsDict['evOverallPerRan']

            # Logging
            Settings.logger.info("Logging EVs")
            Settings.logger.info(f'EV Heuristic: {evOverallHeu}')
            Settings.logger.info(f'EV Random: {evOverallRan}')
            # tensorboard
            tSettings.summary_writer.add_scalar('EV/Heuristic/Overall', evOverallHeu, episodes)
            tSettings.summary_writer.add_scalar('EV/Random/Overall', evOverallRan, episodes)
            tSettings.summary_writer.add_scalar('%/Heuristic/Overall', evOverallPerHeu, episodes)
            tSettings.summary_writer.add_scalar('%/Random/Overall', evOverallPerRan, episodes)
            for i in evPlayerHeu:
                tSettings.summary_writer.add_scalar('EV/Heuristic/' + i[0], i[1], episodes)
            for i in evPlayerRan:
                tSettings.summary_writer.add_scalar('EV/Random/' + i[0], i[1], episodes)
            for i in evPlayerPerHeu:
                tSettings.summary_writer.add_scalar('%/Heuristic/' + i[0], i[1], episodes)
            for i in evPlayerPerRan:
                tSettings.summary_writer.add_scalar('%/Random/' + i[0], i[1], episodes)


if __name__ == '__main__':
    main()
