from collections import namedtuple
from typing import List

from connect4_zero.config import Config
from connect4_zero.env.connect4_env import Connect4Env

CounterKey = namedtuple("CounterKey", "board next_player")
QueueItem = namedtuple("QueueItem", "state future")
HistoryItem = namedtuple("HistoryItem", "action policy values visit")

import numpy as np


# Interface for player class

class BasePlayer:

    def __init__(self, config: Config, play_config=None):
        self.thinking_history = {}  # for fun
        self.labels_n = config.n_labels

        pass

    def action(self, board: List[str]):
        raise NotImplementedError

    @staticmethod
    def counter_key(env: Connect4Env):
        return CounterKey(env.observation, env.turn)

    def ask_thought_about(self, board) -> HistoryItem:
        return self.thinking_history.get(board)

    def get_observation(self, env: Connect4Env):
        return ''.join(''.join(x for x in y) for y in env.board)


class RandomPlayer(BasePlayer):
    def __init__(self, config: Config, play_config=None):
        super().__init__(config, play_config)

    def action(self, board: List[str]):
        env = Connect4Env().update(board)
        key = self.counter_key(env)

        policy = self.uniform_policy()
        action = int(np.random.choice(range(self.labels_n), p=policy))

        return action

    def uniform_policy(self):
        ret = np.zeros(self.labels_n)
        for action in range(len(ret)):
            ret[action] = 1 / len(ret)
        return ret
