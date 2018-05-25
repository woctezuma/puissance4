from ai import AI
from grille import Grille


class MC(AI):
    """Intelligence artificielle reposant sur des simulations Monte-Carlo"""

    def __init__(self, symbole='O', num_tirages_MC=None):
        """Créer un joueur du symbole indiqué"""
        AI.__init__(self, symbole)

        if num_tirages_MC is not None:
            self.num_tirages_MC = num_tirages_MC
        else:
            self.num_tirages_MC = self.get_default_num_tirages_MC()

    @staticmethod
    def get_default_num_tirages_MC():
        return 3

    def get_default_params(self):
        params = super().get_default_params()
        params['num_tirages_MC'] = self.get_default_num_tirages_MC()

        return params

    def print(self):
        super().print()
        print("[Monte Carlo] number of samples = {}".format(self.num_tirages_MC))
        return

    def simuler_monte_carlo(self, grille, current_player):
        """Evaluer une grille par des simulations Monte-Carlo de la fin de la partie"""
        num_victoires = {'O': 0, 'X': 0, 'draw': 0}

        ai = AI(current_player)
        for _ in range(self.num_tirages_MC):
            grille_simulee = Grille(grille)
            winner_symbol = ai.simulate_end_game(grille_simulee)
            num_victoires[winner_symbol] += 1

        try:
            score = (num_victoires[self.get_player_symbol()] - num_victoires[self.get_opponent_symbol()]) \
                    / (num_victoires[self.get_player_symbol()] + num_victoires[self.get_opponent_symbol()])
        except ZeroDivisionError:
            score = 0
        return score

    def play_witout_bias(self, grille):
        """Déterminer la meilleure action en fonction des résultats des simulations Monte-Carlo"""
        meilleure_action = None
        meilleure_evaluation = None
        for action in grille.look_for_allowed_steps():
            grille_simulee = Grille(grille)
            # Le joueur (A) joue un coup.
            grille_simulee.drop(self.player, action)
            # C'est maintenant au tour de l'autre joueur (B).
            # Nous prenons l'opposé de la valeur simulée, car nous nous intéressons au joueur A.
            evaluation = - self.simuler_monte_carlo(grille_simulee, self.get_opponent_symbol())
            if meilleure_evaluation is None or evaluation > meilleure_evaluation:
                meilleure_evaluation = evaluation
                meilleure_action = action
        return meilleure_action
