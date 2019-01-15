from .ai_interface import InterfaceAI
from ..configs.parameters import get_default_bias_to_obvious_steps, get_default_max_num_steps_to_explore


class AI(InterfaceAI):
    """Intelligence artificielle"""

    def __init__(self, symbole='O', bias_to_obvious_steps=None, max_num_steps_to_explore=None):
        super().__init__(symbole)

        if bias_to_obvious_steps is not None:
            self.bias_to_obvious_steps = bias_to_obvious_steps
        else:
            self.bias_to_obvious_steps = get_default_bias_to_obvious_steps()

        if max_num_steps_to_explore is not None:
            self.max_num_steps_to_explore = max_num_steps_to_explore
        else:
            self.max_num_steps_to_explore = get_default_max_num_steps_to_explore()

    def get_default_params(self):
        params = super().get_default_params()
        params['bias_to_obvious_steps'] = get_default_bias_to_obvious_steps()
        params['max_num_steps_to_explore'] = get_default_max_num_steps_to_explore()

        return params

    def print(self):
        super().print()
        print('[End-game simulations] bias to obvious steps = {}'.format(self.bias_to_obvious_steps))
        print('[End-game simulations] maximal number of steps = {}'.format(self.max_num_steps_to_explore))
        return

    def play_witout_bias(self, grille):
        """Jouer de façon non biaisée : renvoyer au hasard un coup possible"""
        return grille.get_random_allowed_step()

    def simulate_end_game(self, grille):
        """Simuler une fin de partie à partir de la grille initiale fournie"""

        player_who_last_played = self.get_opponent_symbol()

        step_counter = 0
        first_action = None

        while not (grille.check_victory()) and len(grille.look_for_allowed_steps()) > 0:
            current_player = self.get_other_symbol(player_who_last_played)

            if self.bias_to_obvious_steps:
                my_play, _ = self.play_with_bias(grille)
            else:
                my_play = self.play_witout_bias(grille)

            if step_counter == 0:
                first_action = my_play

            grille.drop(current_player, my_play)

            player_who_last_played = current_player

            step_counter += 1
            if self.max_num_steps_to_explore is not None and step_counter >= self.max_num_steps_to_explore:
                break

        if grille.check_victory():
            winner_symbol = player_who_last_played
        else:
            winner_symbol = 'draw'

        return winner_symbol, first_action

    # noinspection PyPep8Naming
    def equalize_computing_resources(self, UCT_ai_instance):
        # Give the same computing resources to player X (UCT) and player O (AI):
        super().equalize_computing_resources(UCT_ai_instance)
        try:
            self.bias_to_obvious_steps = UCT_ai_instance.bias_to_obvious_steps
            self.max_num_steps_to_explore = UCT_ai_instance.max_num_steps_to_explore
        except AttributeError:
            print(
                'Equalization of computing resources failed: missing attributes from {}'.format(repr(UCT_ai_instance)))
