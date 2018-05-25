from parameters import get_default_bias_to_obvious_steps, get_default_max_num_steps_to_explore
from win_conditions import look_for_obvious_steps


class AI:
    """Intelligence artificielle"""

    def __init__(self, symbole='O', bias_to_obvious_steps=None, max_num_steps_to_explore=None):
        """Créer un joueur du symbole indiqué"""
        self.player = symbole

        if bias_to_obvious_steps is not None:
            self.bias_to_obvious_steps = bias_to_obvious_steps
        else:
            self.bias_to_obvious_steps = get_default_bias_to_obvious_steps()

        if max_num_steps_to_explore is not None:
            self.max_num_steps_to_explore = max_num_steps_to_explore
        else:
            self.max_num_steps_to_explore = get_default_max_num_steps_to_explore()

    def get_default_params(self):
        params = dict()
        params['bias_to_obvious_steps'] = get_default_bias_to_obvious_steps()
        params['max_num_steps_to_explore'] = get_default_max_num_steps_to_explore()

        return params

    def set_all_parameters_to_default(self):
        self.set_params(self.get_default_params())
        return

    def print(self):
        print()
        print('[AI] symbol = {}'.format(self.player))
        print('[End-game simulations] bias to obvious steps = {}'.format(self.bias_to_obvious_steps))
        print('[End-game simulations] maximal number of steps = {}'.format(self.max_num_steps_to_explore))
        return

    def set_params(self, dico):
        for elem in dico:
            setattr(self, elem, dico[elem])
        return

    def play_witout_bias(self, grille):
        """Jouer de façon non biaisée : renvoyer au hasard un coup possible"""
        return grille.get_random_allowed_step()

    def play_with_bias(self, grille):
        """Jouer de façon biaisée : vérifier s'il est possible de gagner en un coup avant toute réflexion"""
        mon_coup_urgent = look_for_obvious_steps(grille)

        if mon_coup_urgent is None:
            return self.play_witout_bias(grille)
        else:
            return mon_coup_urgent

    def get_player_symbol(self):
        return self.player

    def get_opponent_symbol(self):
        return self.get_other_symbol(self.player)

    @staticmethod
    def get_other_symbol(symbole):
        """Passer du symbole d'un joueur au symbole de son adversaire"""
        if symbole == 'X':
            return 'O'
        else:
            return 'X'

    def simulate_end_game(self, grille):
        """Simuler une fin de partie à partir de la grille initiale fournie"""

        player_who_last_played = self.get_opponent_symbol()

        step_counter = 0

        while not (grille.check_victory()) and len(grille.look_for_allowed_steps()) > 0:
            current_player = self.get_other_symbol(player_who_last_played)

            if self.bias_to_obvious_steps:
                grille.drop(current_player, self.play_with_bias(grille))
            else:
                grille.drop(current_player, self.play_witout_bias(grille))

            player_who_last_played = current_player

            step_counter += 1
            if self.max_num_steps_to_explore is not None and step_counter >= self.max_num_steps_to_explore:
                break

        if grille.check_victory():
            winner_symbol = player_who_last_played
        else:
            winner_symbol = 'draw'

        return winner_symbol
