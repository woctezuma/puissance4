import unittest

import main
import training


class TestMainMethods(unittest.TestCase):

    def test_no_player_for_a_single_game(self):
        self.assertTrue(main.menu('0'))

    def test_no_player_for_many_games(self):
        self.assertTrue(main.menu('3', num_parties_jouees=3))


class TestTrainingMethods(unittest.TestCase):

    def test_prepare_and_train(self):
        self.assertTrue(training.prepare_and_train(num_parties_jouees=3))


if __name__ == '__main__':
    unittest.main()
