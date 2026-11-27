import unittest

from puissance4.env.grille import Grille
from puissance4.env.win_conditions import look_for_obvious_steps

EMPTY_ROWS = ['.......'] * 6


def make_grille(rows):
    grille = Grille()
    grille.set_grid([list(row) for row in rows])
    return grille


def play_moves(moves):
    grille = Grille()
    for symbol, col in moves:
        grille.drop(symbol, col)
    return grille


class TestGrille(unittest.TestCase):
    def test_drop_places_disc_at_the_lowest_empty_row(self):
        grille = Grille()
        self.assertTrue(grille.drop('X', 3))
        self.assertEqual(grille.get_grid()[5][3], 'X')
        self.assertTrue(grille.drop('O', 3))
        self.assertEqual(grille.get_grid()[4][3], 'O')

    def test_drop_in_a_full_column_returns_false(self):
        grille = Grille()
        for _ in range(6):
            self.assertTrue(grille.drop('X', 0))
        self.assertFalse(grille.drop('X', 0))

    def test_look_for_allowed_steps(self):
        grille = Grille()
        self.assertEqual(grille.look_for_allowed_steps(), list(range(7)))
        for _ in range(6):
            grille.drop('X', 2)
        self.assertEqual(grille.look_for_allowed_steps(), [0, 1, 3, 4, 5, 6])

    def test_check_victory_on_empty_grid(self):
        self.assertFalse(Grille().check_victory())

    def test_check_victory_with_three_aligned_discs_only(self):
        rows = list(EMPTY_ROWS)
        rows[5] = 'XXX....'
        self.assertFalse(make_grille(rows).check_victory())

    def test_check_victory_horizontal(self):
        rows = list(EMPTY_ROWS)
        rows[5] = 'XXXX...'
        self.assertTrue(make_grille(rows).check_victory())

    def test_check_victory_vertical(self):
        rows = list(EMPTY_ROWS)
        rows[2] = '.X.....'
        rows[3] = '.X.....'
        rows[4] = '.X.....'
        rows[5] = '.X.....'
        self.assertTrue(make_grille(rows).check_victory())

    def test_check_victory_diagonal_descending(self):
        rows = list(EMPTY_ROWS)
        rows[2] = 'X......'
        rows[3] = '.X.....'
        rows[4] = '..X....'
        rows[5] = '...X...'
        self.assertTrue(make_grille(rows).check_victory())

    def test_check_victory_diagonal_ascending(self):
        rows = list(EMPTY_ROWS)
        rows[2] = '...X...'
        rows[3] = '..X....'
        rows[4] = '.X.....'
        rows[5] = 'X......'
        self.assertTrue(make_grille(rows).check_victory())

    def test_copy_is_a_deep_copy(self):
        grille = Grille()
        grille.drop('X', 0)
        clone = Grille()
        clone.copy(grille)
        grille.drop('O', 0)
        self.assertEqual(clone.get_num_steps(), 1)
        self.assertEqual(clone.get_grid()[5][0], 'X')

    def test_name_round_trip(self):
        rows = list(EMPTY_ROWS)
        rows[5] = 'X.O....'
        grille = make_grille(rows)
        clone = Grille()
        clone.copy_name(grille.get_name())
        self.assertEqual(clone.get_grid(), grille.get_grid())


class TestObviousSteps(unittest.TestCase):
    def test_winning_step_is_found(self):
        rows = list(EMPTY_ROWS)
        rows[5] = 'XXX....'
        grille = make_grille(rows)
        self.assertFalse(grille.check_victory())
        self.assertEqual(look_for_obvious_steps(grille, 'X', 'O'), 3)

    def test_opponent_threat_is_blocked(self):
        rows = list(EMPTY_ROWS)
        rows[5] = 'OOO....'
        grille = make_grille(rows)
        self.assertEqual(look_for_obvious_steps(grille, 'X', 'O'), 3)

    def test_winning_step_is_preferred_over_blocking(self):
        rows = list(EMPTY_ROWS)
        rows[5] = 'OOOXXX.'
        grille = make_grille(rows)
        self.assertEqual(look_for_obvious_steps(grille, 'X', 'O'), 6)

    def test_vertical_winning_step_is_found(self):
        grille = play_moves([('X', 0), ('O', 1), ('X', 0), ('O', 1), ('X', 0)])
        self.assertEqual(look_for_obvious_steps(grille, 'X', 'O'), 0)

    def test_diagonal_ascending_winning_step_is_found(self):
        grille = play_moves(
            [
                ('X', 0),
                ('O', 1),
                ('X', 1),
                ('O', 2),
                ('O', 2),
                ('X', 2),
                ('O', 3),
                ('X', 3),
                ('O', 3),
            ],
        )
        self.assertEqual(look_for_obvious_steps(grille, 'X', 'O'), 3)
        grille.drop('X', 3)
        self.assertTrue(grille.check_victory())

    def test_diagonal_descending_winning_step_is_found(self):
        grille = play_moves(
            [
                ('O', 0),
                ('O', 0),
                ('O', 0),
                ('O', 1),
                ('O', 1),
                ('X', 1),
                ('O', 2),
                ('X', 2),
                ('X', 3),
            ],
        )
        self.assertEqual(look_for_obvious_steps(grille, 'X', 'O'), 0)
        grille.drop('X', 0)
        self.assertTrue(grille.check_victory())

    def test_no_obvious_step(self):
        rows = list(EMPTY_ROWS)
        rows[5] = 'X......'
        grille = make_grille(rows)
        self.assertIsNone(look_for_obvious_steps(grille, 'X', 'O'))


if __name__ == '__main__':
    unittest.main()
