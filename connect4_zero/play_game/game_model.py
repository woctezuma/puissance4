from logging import getLogger

from connect4_zero.agent.player_connect4 import HistoryItem
from connect4_zero.agent.player_connect4 import Player
from connect4_zero.agent.player_interface import RandomPlayer
from connect4_zero.config import Config

logger = getLogger(__name__)


class PlayWithHuman:
    def __init__(self, config: Config):
        self.config = config
        self.human_color = None
        self.observers = []
        self.ai = None  # type: BasePlayer
        self.last_evaluation = None
        self.last_history = None  # type: HistoryItem

    def start_game(self, human_is_black):
        self.human_color = Player.black if human_is_black else Player.white
        # self.ai = Connect4Player(self.config)
        self.ai = RandomPlayer(self.config)

    def move_by_ai(self, env):
        action = self.ai.action(env.board)

        if self.last_history is not None:
            self.last_history = self.ai.ask_thought_about(env.observation)
            self.last_evaluation = self.last_history.values[self.last_history.action]
            if self.human_color == Player.black:
                logger.debug(f"evaluation by ai={self.last_evaluation}")
            else:
                logger.debug(f"evaluation by ai={-self.last_evaluation}")

        return action

    def move_by_human(self, env):
        while True:
            try:
                movement = input('\nEnter your movement (1, 2, 3, 4, 5, 6, 7): ')
                movement = int(movement) - 1
                legal_moves = env.legal_moves()
                if legal_moves[int(movement)] == 1:
                    return int(movement)
                else:
                    print("That is NOT a valid movement :(.")
            except:
                print("That is NOT a valid movement :(.")
