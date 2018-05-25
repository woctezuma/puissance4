from parameters import get_default_player_symbol, get_default_check_obvious_plays
from win_conditions import look_for_obvious_steps


class InterfaceAI:
    def __init__(self, symbole=None, check_obvious_plays=None):
        """Créer un joueur du symbole indiqué"""
        if symbole is not None:
            self.player = symbole
        else:
            self.player = get_default_player_symbol()

        if check_obvious_plays is not None:
            self.check_obvious_plays = check_obvious_plays
        else:
            self.check_obvious_plays = get_default_check_obvious_plays()

    def get_default_params(self):
        params = dict()
        params['player'] = get_default_player_symbol()
        params['check_obvious_plays'] = get_default_check_obvious_plays()

        return params

    def print(self):
        print()
        print('[AI] symbol = {}'.format(self.player))
        print('[AI] bias to obvious steps = {}'.format(self.check_obvious_plays))

    def play_witout_bias(self, grille):
        raise NotImplementedError

    def simulate_end_game(self, grille):
        raise NotImplementedError

    def play(self, grille):
        if self.check_obvious_plays:
            return self.play_with_bias(grille)
        else:
            return self.play_witout_bias(grille)

    def set_params(self, dico):
        for elem in dico:
            setattr(self, elem, dico[elem])
        return

    def set_all_parameters_to_default(self):
        self.set_params(self.get_default_params())
        return

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
