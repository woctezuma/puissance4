import unittest

import puissance4


class TestTrainingMethods(unittest.TestCase):

    def test_prepare_and_train(self):
        is_consistent, _, _ = puissance4.prepare_and_train(trainer_choice='Random',
                                                                    num_parties_jouees=10)
        self.assertTrue(is_consistent)

    def test_prepare_and_train_vs_monte_carlo(self):
        is_consistent_deterministic, _, _ = puissance4.prepare_and_train(trainer_choice='MC',
                                                                                  num_parties_jouees=10,
                                                                                  deterministic_root_action_sample=True)
        self.assertTrue(is_consistent_deterministic)

        is_consistent_random, _, _ = puissance4.prepare_and_train(trainer_choice='MC',
                                                                           num_parties_jouees=10,
                                                                           deterministic_root_action_sample=False)
        self.assertTrue(is_consistent_random)

    def test_prepare_and_train_vs_self(self):
        is_consistent, _, _ = puissance4.prepare_and_train(trainer_choice='UCT',
                                                                    num_parties_jouees=10)
        self.assertTrue(is_consistent)

    def test_save_then_load_model(self):
        is_consistent_save, _, _ = puissance4.prepare_and_train(trainer_choice='Random',
                                                                         num_parties_jouees=3,
                                                                         load_and_save_previously_trained_model=True)

        self.assertTrue(is_consistent_save)

        is_consistent_load, _, _ = puissance4.prepare_and_train(trainer_choice='MC',
                                                                         num_parties_jouees=3,
                                                                         load_and_save_previously_trained_model=True)

        self.assertTrue(is_consistent_load)


if __name__ == '__main__':
    unittest.main()
