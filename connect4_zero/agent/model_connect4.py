from logging import getLogger

from connect4_zero.config import Config

logger = getLogger(__name__)


class Connect4Model:
    def __init__(self, config: Config):
        self.config = config
        self.model = None  # type: Model
        self.digest = None

    def predict_on_batch(self, x):
        """

        :param x: a numpy array which shape is (1, 2, 6, 7), with the 6x7 board stored as both x[0][0] and x[0][1]
        :return policy: a list
        :return value: a list
        """
        raise NotImplementedError
        #
        # from random import randint
        #
        # policy = [randint(0,7) for _ in range(20)]
        # value = [randint(-100,100) for _ in range(len(policy))]
        #
        # return policy, value
