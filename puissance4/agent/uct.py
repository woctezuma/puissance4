import pathlib
from math import sqrt, log
from random import choice

from .mc import MC
from ..configs.parameters import get_default_num_descentes_dans_arbre, get_default_facteur_uct
from ..env.grille import Grille
from ..lib.node import Node


class UCT(MC):
    """Intelligence artificielle reposant sur l'algorithme Upper-Confidence-Tree"""

    def __init__(self, symbole='O', num_descentes_dans_arbre=None, facteur_uct=None):
        super().__init__(symbole)

        if num_descentes_dans_arbre is not None:
            self.num_descentes_dans_arbre = num_descentes_dans_arbre
        else:
            self.num_descentes_dans_arbre = get_default_num_descentes_dans_arbre()

        if facteur_uct is not None:
            self.facteur_uct = facteur_uct
        else:
            self.facteur_uct = get_default_facteur_uct()

        self.dict_num_visits_of_board_state = dict()
        self.dict_for_action_in_board_state = dict()
        self.tree = None

        self.data_path = 'data/'
        self.node_visit_filename = 'node_visit.txt'
        self.node_action_filename = 'node_action.txt'

    def load_model(self):
        # NB: It is apparently useless to load these variables for different games.

        try:

            import ast

            with open(self.data_path + self.node_visit_filename, 'r', encoding="utf8") as f:
                self.dict_num_visits_of_board_state = ast.literal_eval(f.readlines()[0])

            with open(self.data_path + self.node_action_filename, 'r', encoding="utf8") as f:
                self.dict_for_action_in_board_state = ast.literal_eval(f.readlines()[0])

        except FileNotFoundError:
            print('Model files cound not be loaded.')

        return

    def save_model(self):
        # NB: It is apparently useless to save these variables for different games.

        # Reference of the following line: https://stackoverflow.com/a/14364249
        pathlib.Path(self.data_path).mkdir(parents=True, exist_ok=True)

        with open(self.data_path + self.node_visit_filename, 'w', encoding="utf8") as f:
            print(self.dict_num_visits_of_board_state, file=f)

        with open(self.data_path + self.node_action_filename, 'w', encoding="utf8") as f:
            print(self.dict_for_action_in_board_state, file=f)

        return

    def get_default_params(self):
        params = super().get_default_params()
        params['num_descentes_dans_arbre'] = get_default_num_descentes_dans_arbre()
        params['facteur_uct'] = get_default_facteur_uct()

        return params

    def print(self):
        super().print()
        print("[Upper Confidence Tree] number of tree descents = {}".format(self.num_descentes_dans_arbre))
        print("[Upper Confidence Tree] UCT factor = {}".format(self.facteur_uct))
        return

    @classmethod
    def print_strategy(cls):
        return

    def play_witout_bias(self, grille):
        """Déterminer la meilleure action en fonction des résultats de l'exploration UCT"""
        # recevoir une position p
        initial_board_state = grille.get_name()
        # soit A l'arbre UCT vide à la racine près
        self.tree = Node(initial_board_state)
        # boucle : plusieurs descentes dans l'arbre
        for _ in range(self.num_descentes_dans_arbre):
            # soit N le noeud résultant d'une descente dans l'arbre (A, p)
            (N, current_player_at_N) = self.tree_down()
            # soit R l'évaluation de p
            grille_copiee = Grille()
            grille_copiee.copy_name(N.name)

            # noinspection PyPep8Naming
            R, _ = self.simuler_monte_carlo(grille_copiee, current_player_at_N)
            # Attention! R est la valeur pour 'current_player_at_N', pas forcément pour 'self.player'!

            # nous effectuons une remontée de l'arbre (A, N, R)
            self.tree_up(N, R, current_player_at_N)
        # renvoyer le coup fils (de la racine de A) qui a la meilleure valeur UCT
        meilleure_action = self.choisir_action_uct(grille)
        return meilleure_action

    def tree_down(self):
        """Descendre dans l'arbre UCT"""
        # Initialisation des variables (N, current_player, grille) avant la boucle while

        # soit N la racine de l'arbre
        # noinspection PyPep8Naming
        N = self.tree

        current_player = self.player

        grille = Grille()
        grille.copy_name(N.name)

        # boucle : fils non explorés de N
        while all([(N.name, i) in self.dict_for_action_in_board_state for i in grille.look_for_allowed_steps()]):
            # soit F le fils de N ayant la plus grande valeur UCT
            if len(grille.look_for_allowed_steps()) > 0:
                action = self.choisir_action_uct(grille)
                nouvel_etat = self.changer_etat_apres_transition(N.name, action, current_player)
                f = Node(nouvel_etat, N)
                f.code = action

                # noinspection PyPep8Naming
                N = f
                current_player = self.get_other_symbol(current_player)
                grille.copy_name(N.name)

            else:
                break

        # soir F un fils de N tiré au hasard parmi les fils non explorés
        mes_coups_possibles = grille.look_for_allowed_steps()
        if len(mes_coups_possibles) > 0:
            actions_inexplorees = [i for i in mes_coups_possibles if
                                   (N.name, i) not in self.dict_for_action_in_board_state]
            action = choice(actions_inexplorees)
            etat_inexplore = self.changer_etat_apres_transition(N.name, action, current_player)
            f = Node(etat_inexplore, N)
            f.code = action

            current_player = self.get_other_symbol(current_player)
        else:
            f = N
        return f, current_player

    # noinspection PyPep8Naming
    def tree_up(self, node_N, value_R, current_player_at_N):
        """Remonter dans l'arbre UCT"""
        current_player = current_player_at_N

        while node_N is not self.tree:
            parent_board_state = node_N.parent.name
            action_to_reach_N = node_N.code

            try:
                self.dict_num_visits_of_board_state[node_N.name] += 1
            except KeyError:
                self.dict_num_visits_of_board_state[node_N.name] = 1

            try:
                self.dict_for_action_in_board_state[(parent_board_state, action_to_reach_N)]['count'] += 1
            except KeyError:
                self.dict_for_action_in_board_state[(parent_board_state, action_to_reach_N)] = dict()
                self.dict_for_action_in_board_state[(parent_board_state, action_to_reach_N)]['count'] = 1

            symbol_for_parent_of_current_player = self.get_other_symbol(current_player)

            # R is the valuation of Node N, in the best interest of 'current_player_at_N'.
            # However, q is the valuation of the PARENT of 'current_player', which means that:
            # q = R if the PARENT of current player shares its symbol with Node N,
            # q = -R if the PARENT of current player does not share its symbol with Node N.
            #
            if current_player != current_player_at_N:  # <- La ligne qui m'a fait perdre beaucoup de temps.
                q = value_R
            else:
                q = - value_R

            try:
                # En effet, nous nous intéressons au parent de N, et non à N lui-même.
                mu_avant = self.dict_for_action_in_board_state[(parent_board_state, action_to_reach_N)]['score']
            except KeyError:
                mu_avant = 0

            n = self.dict_for_action_in_board_state[(parent_board_state, action_to_reach_N)]['count']
            mu = mu_avant + (1.0 / n) * (q - mu_avant)
            self.dict_for_action_in_board_state[(parent_board_state, action_to_reach_N)]['score'] = mu

            node_N = node_N.parent
            current_player = symbol_for_parent_of_current_player

        # Enfin, visite de la racine.
        try:
            self.dict_num_visits_of_board_state[node_N.name] += 1
        except KeyError:
            self.dict_num_visits_of_board_state[node_N.name] = 1

        return

    def choisir_action_uct(self, grille):
        """Choisir une action en utilisant le critère UCB"""
        etat = grille.get_name()
        meilleure_action = None
        meilleure_evaluation = None
        for action in grille.look_for_allowed_steps():
            if (etat, action) not in self.dict_for_action_in_board_state:
                continue
            recompense_moyenne = self.dict_for_action_in_board_state[(etat, action)]['score']
            num_etat_action = self.dict_for_action_in_board_state[(etat, action)]['count']
            num_etat = self.dict_num_visits_of_board_state[etat]
            evaluation = recompense_moyenne + self.facteur_uct * sqrt(1.0 * log(num_etat) / num_etat_action)
            if meilleure_evaluation is None or evaluation > meilleure_evaluation:
                meilleure_evaluation = evaluation
                meilleure_action = action
        if meilleure_action is None:
            print("Aucun coup admissible.")
        return meilleure_action

    @staticmethod
    def changer_etat_apres_transition(etat, action, joueur):
        """Déterminer l'état obtenu lorsque le joueur effectue l'action dans l'état donné"""
        grille_copiee = Grille()
        grille_copiee.copy_name(etat)
        grille_copiee.drop(joueur, action)
        nouvel_etat = grille_copiee.get_name()
        return nouvel_etat

    # noinspection PyPep8Naming
    def equalize_computing_resources(self, UCT_ai_instance):
        # Give the same computing resources to player X (UCT) and player O (UCT):
        super().equalize_computing_resources(UCT_ai_instance)
        try:

            # Override the value set by superclass MC
            self.num_tirages_MC = UCT_ai_instance.num_tirages_MC

            # Set values for class UCT
            self.num_descentes_dans_arbre = UCT_ai_instance.num_descentes_dans_arbre
            self.facteur_uct = UCT_ai_instance.facteur_uct

        except AttributeError:
            print(
                'Equalization of computing resources failed: missing attributes from {}'.format(repr(UCT_ai_instance)))
