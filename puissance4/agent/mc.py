import operator

from .ai import AI
from ..configs.parameters import get_default_num_tirages_MC, get_default_action_sampling_strategy
from ..env.grille import Grille


class MC(AI):
    """Intelligence artificielle reposant sur des simulations Monte-Carlo"""

    # noinspection PyPep8Naming
    def __init__(self, symbole='O', num_tirages_MC=None, deterministic_sampling_of_actions_at_root=None):
        super().__init__(symbole)

        if num_tirages_MC is not None:
            self.num_tirages_MC = num_tirages_MC
        else:
            self.num_tirages_MC = get_default_num_tirages_MC()

        if deterministic_sampling_of_actions_at_root is not None:
            self.deterministic_sampling_of_actions_at_root = deterministic_sampling_of_actions_at_root
        else:
            self.deterministic_sampling_of_actions_at_root = get_default_action_sampling_strategy()

    def get_default_params(self):
        params = super().get_default_params()
        params['num_tirages_MC'] = get_default_num_tirages_MC()
        params['deterministic_sampling_of_actions_at_root'] = get_default_action_sampling_strategy()

        return params

    def print(self):
        super().print()
        print("[Monte Carlo] number of samples for grid valuation = {}".format(self.num_tirages_MC))
        self.print_strategy()
        return

    def print_strategy(self):
        print("[Monte Carlo] deterministic strategy for action sampling at the root = {}".format(
            self.deterministic_sampling_of_actions_at_root))
        return

    def play_witout_bias(self, grille):
        """Déterminer la meilleure action en fonction des résultats des simulations Monte-Carlo"""
        meilleure_action = None

        allowed_steps = grille.look_for_allowed_steps()

        if len(allowed_steps) == 1:
            meilleure_action = allowed_steps[0]
        elif len(allowed_steps) > 1:
            if self.deterministic_sampling_of_actions_at_root:
                meilleure_action = self.uniformly_sample_actions_at_root(grille, allowed_steps)
            else:
                meilleure_action = self.randomly_sample_actions_at_root(grille)

        return meilleure_action

    def randomly_sample_actions_at_root(self, grille, num_end_game_simulations=None):

        if num_end_game_simulations is None:
            num_end_game_simulations = self.num_tirages_MC

        # C'est au tour du joueur (A).
        current_player = self.get_player_symbol()

        _, meilleure_action = self.simuler_monte_carlo(grille, current_player, num_end_game_simulations)

        return meilleure_action

    def uniformly_sample_actions_at_root(self, grille, allowed_steps=None, num_end_game_simulations=None):

        if allowed_steps is None:
            allowed_steps = grille.look_for_allowed_steps()

        if num_end_game_simulations is None:
            num_end_game_simulations = 1 + (self.num_tirages_MC // len(allowed_steps))

        meilleure_action = None
        meilleure_evaluation = None

        for action in allowed_steps:

            grille_simulee = Grille(grille)
            # Le joueur (A) joue un coup.
            grille_simulee.drop(self.player, action)
            # C'est maintenant au tour de l'autre joueur (B).
            R, _ = self.simuler_monte_carlo(grille_simulee, self.get_opponent_symbol(), num_end_game_simulations)
            # Nous prenons l'opposé de la valeur simulée, car nous nous intéressons au joueur A.
            evaluation = - R

            if meilleure_evaluation is None or evaluation > meilleure_evaluation:
                meilleure_evaluation = evaluation
                meilleure_action = action

        return meilleure_action

    def simuler_monte_carlo(self, grille, current_player, num_end_game_simulations=None):
        """
        Evaluer une grille par des simulations Monte-Carlo de la fin de la partie

        Attention! La valeur renvoyée correspond à l'estimation pour "current_player", et pas nécessairement
        pour "self.player" !
        """

        if num_end_game_simulations is None:
            num_end_game_simulations = self.num_tirages_MC

        victory_stats_for_first_actions = self.core_process_monte_carlo(grille, current_player,
                                                                        num_end_game_simulations)

        best_grid_valuation, best_first_action = self.post_process_monte_carlo(victory_stats_for_first_actions,
                                                                               current_player)

        return best_grid_valuation, best_first_action

    def core_process_monte_carlo(self, grille, current_player, num_end_game_simulations=None):

        if num_end_game_simulations is None:
            num_end_game_simulations = self.num_tirages_MC

        victory_stats_for_first_actions = dict()

        # Warning: this is a random AI, so you might want to use values different from the defaults used by MC for:
        # - self.bias_to_obvious_steps
        # - self.max_num_steps_to_explore
        ai = AI(current_player, self.bias_to_obvious_steps, self.max_num_steps_to_explore)

        for _ in range(num_end_game_simulations):
            grille_simulee = Grille(grille)
            winner_symbol, first_action = ai.simulate_end_game(grille_simulee)

            try:
                victory_stats_for_first_actions[first_action][winner_symbol] += 1
            except KeyError:
                victory_stats_for_first_actions[first_action] = {'O': 0, 'X': 0, 'draw': 0}
                victory_stats_for_first_actions[first_action][winner_symbol] += 1

        return victory_stats_for_first_actions

    def post_process_monte_carlo(self, victory_stats_for_first_actions, current_player):

        grid_valuations_for_first_actions = self.find_grid_valuations_for_first_actions(victory_stats_for_first_actions,
                                                                                        current_player)

        best_first_action = self.find_best_first_action(grid_valuations_for_first_actions)

        best_grid_valuation = self.find_best_grid_valuation(grid_valuations_for_first_actions, best_first_action)

        return best_grid_valuation, best_first_action

    def find_grid_valuations_for_first_actions(self, victory_stats_for_first_actions, player_symbol):
        # Compute a score based on the stats of victories

        opponent_symbol = self.get_other_symbol(player_symbol)

        grid_valuations_for_first_actions = dict()
        for (action, num_victoires) in victory_stats_for_first_actions.items():

            try:
                action_score = (num_victoires[player_symbol] - num_victoires[opponent_symbol]) \
                               / (num_victoires[player_symbol] + num_victoires[opponent_symbol]
                                  + num_victoires['draw'])
            except ZeroDivisionError:
                action_score = 0

            grid_valuations_for_first_actions[action] = action_score

        return grid_valuations_for_first_actions

    @classmethod
    def find_best_first_action(cls, grid_valuations_for_first_actions):
        # Reference: https://stackoverflow.com/a/268285
        best_first_action = max(grid_valuations_for_first_actions.items(), key=operator.itemgetter(1))[0]
        return best_first_action

    def find_best_grid_valuation(self, grid_valuations_for_first_actions, best_first_action=None):
        if best_first_action is None:
            best_first_action = self.find_best_first_action(grid_valuations_for_first_actions)
        best_grid_valuation = grid_valuations_for_first_actions[best_first_action]
        return best_grid_valuation

    # noinspection PyPep8Naming
    def equalize_computing_resources(self, UCT_ai_instance):
        # Give the same computing resources to player X (UCT) and player O (MC):
        super().equalize_computing_resources(UCT_ai_instance)
        try:
            # By increasing 'num_tirages_MC', the TOTAL number of MC samples should be ABOUT the same as for UCT.
            # NB: - ABOUT the same for the deterministic case uniformly_sample_actions_at_root().
            #     - EXACTLY the same for the non-deterministic case randomly_sample_actions_at_root().
            self.num_tirages_MC = UCT_ai_instance.num_tirages_MC * UCT_ai_instance.num_descentes_dans_arbre

            # NB: grid valuation depends on another parameter ('num_end_game_simulations') which is:
            # - computed on the fly for the deterministic case, so that the TOTAL number of samples is about as expected
            # - equal to 'num_tirages_MC' for the non-deterministic case.

        except AttributeError:
            print(
                'Equalization of computing resources failed: missing attributes from {}'.format(repr(UCT_ai_instance)))
