import unittest

import main


class TestMainMethods(unittest.TestCase):

    def test_no_player_for_a_single_game(self):
        self.assertTrue(main.menu('0'))

    def test_no_player_for_many_games(self):
        self.assertTrue(main.menu('3'))


if __name__ == '__main__':
    unittest.main()
