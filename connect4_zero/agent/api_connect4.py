from connect4_zero.config import Config


class Connect4ModelAPI:
    def __init__(self, config: Config):
        self.config = config

    def predict(self, x):
        assert x.ndim in (3, 4)
        assert x.shape == (2, 6, 7) or x.shape[1:] == (2, 6, 7)
        orig_x = x
        if x.ndim == 3:
            x = x.reshape(1, 2, 6, 7)
        policy, value = self.predict_on_batch(x)

        if orig_x.ndim == 3:
            return policy[0], value[0]
        else:
            return policy, value

    def predict_on_batch(self, x):
        """

        :param x: a numpy array which shape is (1, 2, 6, 7), with the 6x7 board stored as both x[0][0] and x[0][1]
        :return policy: a list
        :return value: a list
        """

        # TODO

        # policy = range(7)
        # value = [i % 2 == 1 for i in policy]
        #
        # return policy, value

        raise NotImplementedError
