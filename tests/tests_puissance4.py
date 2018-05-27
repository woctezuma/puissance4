import unittest

import puissance4


class TestTrainingMethods(unittest.TestCase):

    def test_prepare_and_train(self):
        is_consistent, num_victories, num_steps = puissance4.prepare_and_train(trainer_choice='Random',
                                                                               num_parties_jouees=200)
        self.assertTrue(is_consistent)


if __name__ == '__main__':
    unittest.main()
