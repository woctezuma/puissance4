from ai import AI
from grille import Grille
from parameters import get_default_num_tirages_MC


class MC(AI):
    """Intelligence artificielle reposant sur des simulations Monte-Carlo"""

    # noinspection PyPep8Naming
    def __init__(self, symbole='O', num_tirages_MC=None):
        super().__init__(symbole)

        if num_tirages_MC is not None:
            self.num_tirages_MC = num_tirages_MC
        else:
            self.num_tirages_MC = get_default_num_tirages_MC()

    def get_default_params(self):
        params = super().get_default_params()
        params['num_tirages_MC'] = get_default_num_tirages_MC()

        return params

    def print(self):
        super().print()
        print("[Monte Carlo] number of samples = {}".format(self.num_tirages_MC))
        return

    def play_witout_bias(self, grille):
        """Déterminer la meilleure action en fonction des résultats des simulations Monte-Carlo"""
        meilleure_action = None
        meilleure_evaluation = None

        allowed_steps = grille.look_for_allowed_steps()
        if len(allowed_steps) > 0:
            num_end_game_simulations = 1 + (self.num_tirages_MC // len(allowed_steps))
        else:
            num_end_game_simulations = None

        for action in allowed_steps:
            grille_simulee = Grille(grille)
            # Le joueur (A) joue un coup.
            grille_simulee.drop(self.player, action)
            # C'est maintenant au tour de l'autre joueur (B).
            # Nous prenons l'opposé de la valeur simulée, car nous nous intéressons au joueur A.
            evaluation = - self.simuler_monte_carlo(grille_simulee, self.get_opponent_symbol(),
                                                    num_end_game_simulations)
            if meilleure_evaluation is None or evaluation > meilleure_evaluation:
                meilleure_evaluation = evaluation
                meilleure_action = action
        return meilleure_action

    def simuler_monte_carlo(self, grille, current_player, num_end_game_simulations=None):
        """
        Evaluer une grille par des simulations Monte-Carlo de la fin de la partie

        Attention! La valeur renvoyée correspond à l'estimation pour "current_player", et pas nécessairement pour "self.player" !
        """

        if num_end_game_simulations is None:
            num_end_game_simulations = self.num_tirages_MC

        num_victoires = {'O': 0, 'X': 0, 'draw': 0}

        # Warning: this is a random AI, so you might want to use values different from the defaults used by MC for:
        # - self.bias_to_obvious_steps
        # - self.max_num_steps_to_explore
        ai = AI(current_player, self.bias_to_obvious_steps, self.max_num_steps_to_explore)

        for _ in range(num_end_game_simulations):
            grille_simulee = Grille(grille)
            winner_symbol = ai.simulate_end_game(grille_simulee)
            num_victoires[winner_symbol] += 1

        try:
            score = (num_victoires[ai.get_player_symbol()] - num_victoires[ai.get_opponent_symbol()]) \
                    / (num_victoires[ai.get_player_symbol()] + num_victoires[ai.get_opponent_symbol()]
                       + num_victoires['draw'])
        except ZeroDivisionError:
            score = 0
        return score

    # noinspection PyPep8Naming
    def equalize_computing_resources(self, UCT_ai_instance):
        # Give the same computing resources to player X (UCT) and player O (MC):
        try:
            self.num_tirages_MC = UCT_ai_instance.num_tirages_MC * UCT_ai_instance.num_descentes_dans_arbre
        except AttributeError:
            print(
                'Equalization of computing resources failed: missing attributes from {}'.format(repr(UCT_ai_instance)))
