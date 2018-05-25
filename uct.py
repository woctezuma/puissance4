import pathlib
import pickle
from math import sqrt, log
from random import choice

from grille import Grille
from mc import MC
from node import Node
from parameters import get_default_num_descentes_dans_arbre, get_default_facteur_uct


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

        self.compteur_visite_etat = {}
        self.score_choix_action_dans_etat = {}
        self.compteur_choix_action_dans_etat = {}
        self.tree = None

        self.data_path = 'data/'
        self.node_visit_filename = 'node_visit.pickle'
        self.action_score_filename = 'action_score.pickle'
        self.action_count_filename = 'action_count.pickle'
        self.tree_filename = 'tree.pickle'

    def load_model(self):

        try:

            with open(self.data_path + self.node_visit_filename, 'rb') as f:
                self.compteur_visite_etat = pickle.load(f)

            with open(self.data_path + self.action_score_filename, 'rb') as f:
                self.score_choix_action_dans_etat = pickle.load(f)

            with open(self.data_path + self.action_count_filename, 'rb') as f:
                self.compteur_choix_action_dans_etat = pickle.load(f)

            with open(self.data_path + self.tree_filename, 'rb') as f:
                self.tree = pickle.load(f)

        except FileNotFoundError:
            print('Model files cound not be loaded.')

        return

    def save_model(self):

        # Reference of the following line: https://stackoverflow.com/a/14364249
        pathlib.Path(self.data_path).mkdir(parents=True, exist_ok=True)

        with open(self.data_path + self.node_visit_filename, 'wb') as f:
            pickle.dump(self.compteur_visite_etat, f, pickle.HIGHEST_PROTOCOL)

        with open(self.data_path + self.action_score_filename, 'wb') as f:
            pickle.dump(self.score_choix_action_dans_etat, f, pickle.HIGHEST_PROTOCOL)

        with open(self.data_path + self.action_count_filename, 'wb') as f:
            pickle.dump(self.compteur_choix_action_dans_etat, f, pickle.HIGHEST_PROTOCOL)

        with open(self.data_path + self.tree_filename, 'wb') as f:
            pickle.dump(self.tree, f, pickle.HIGHEST_PROTOCOL)

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
            R = self.simuler_monte_carlo(grille_copiee, current_player_at_N)
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
        while all([(N.name, i) in self.compteur_choix_action_dans_etat for i in grille.look_for_allowed_steps()]):
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
                                   (N.name, i) not in self.compteur_choix_action_dans_etat]
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
                self.compteur_visite_etat[node_N.name] += 1
            except KeyError:
                self.compteur_visite_etat[node_N.name] = 1

            try:
                self.compteur_choix_action_dans_etat[(parent_board_state, action_to_reach_N)] += 1
            except KeyError:
                self.compteur_choix_action_dans_etat[(parent_board_state, action_to_reach_N)] = 1

            q = value_R
            # Pour information, la ligne ci-dessous est juste, ne pas mettre de signe "!=" au lieu de "==".
            if current_player == current_player_at_N:  # <- La ligne qui m'a fait perdre beaucoup de temps.
                q *= -1.0

            try:
                # En effet, nous nous intéressons au parent de N, et non à N lui-même.
                mu_avant = self.score_choix_action_dans_etat[(parent_board_state, action_to_reach_N)]
            except KeyError:
                mu_avant = 0

            n = self.compteur_choix_action_dans_etat[(parent_board_state, action_to_reach_N)]
            mu = mu_avant + (1.0 / n) * (q - mu_avant)
            self.score_choix_action_dans_etat[(parent_board_state, action_to_reach_N)] = mu

            node_N = node_N.parent
            current_player = self.get_other_symbol(current_player)

        # Enfin, visite de la racine.
        try:
            self.compteur_visite_etat[node_N.name] += 1
        except KeyError:
            self.compteur_visite_etat[node_N.name] = 1

        return

    def choisir_action_uct(self, grille):
        """Choisir une action en utilisant le critère UCB"""
        etat = grille.get_name()
        meilleure_action = None
        meilleure_evaluation = None
        for action in grille.look_for_allowed_steps():
            if (etat, action) not in self.score_choix_action_dans_etat:
                continue
            recompense_moyenne = self.score_choix_action_dans_etat[(etat, action)]
            num_etat_action = self.compteur_choix_action_dans_etat[(etat, action)]
            num_etat = self.compteur_visite_etat[etat]
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
