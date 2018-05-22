from math import sqrt, log
from random import randint

from grille import Grille
from mc import MC, get_other_symbol
from node import Node


class UCT(MC):
    """Intelligence artificielle reposant sur l'algorithme Upper-Confidence-Tree"""

    def __init__(self, symbole='O', num_tirages_m_c=3, num_descentes_dans_arbre=7, facteur_uct=0.0):
        """Créer un joueur du symbole indiqué"""
        MC.__init__(self, symbole, num_tirages_m_c)
        self.compteur_visite_etat = {}
        self.score_choix_action_dans_etat = {}
        self.compteur_choix_action_dans_etat = {}
        self.num_descentes_dans_arbre = num_descentes_dans_arbre
        self.facteur_uct = facteur_uct
        self.tree = None

    def set_tree(self, input_tree):
        self.tree = input_tree

    def play_witout_bias(self, grille):
        """Déterminer la meilleure action en fonction des résultats de l'exploration UCT"""
        # recevoir une position p
        etat_initial = grille.get_name()
        symbole_dont_c_est_le_tour = self.player
        # soit A l'arbre UCT vide à la racine près
        self.set_tree(Node(etat_initial))
        # boucle : plusieurs descentes dans l'arbre
        for _ in range(self.num_descentes_dans_arbre):
            # soit p' une copie de p
            grille_copiee = Grille()
            grille_copiee.set(etat_initial)
            # soit N le noeud résultat d'une descente dans l'arbre (A, p')
            (N, symbole_dont_c_est_le_tour_pour_N) = self.tree_down(grille_copiee, symbole_dont_c_est_le_tour)
            # soit R l'évaluation de p'
            grille_pour__n = N.name
            grille_simulee = Grille()
            grille_simulee.set(grille_pour__n)
            r = self.simuler_monte_carlo(grille_simulee, symbole_dont_c_est_le_tour_pour_N)
            # nous effectuons une remontée de l'arbre (A, N, R)
            self.tree_up(N, r, symbole_dont_c_est_le_tour, symbole_dont_c_est_le_tour_pour_N)
        # renvoyer le coup fils (de la racine de A) qui a la meilleure valeur UCT
        meilleure_action = self.choisir_action_uct(grille)
        return meilleure_action

    def tree_down(self, position_courante, symbole_dont_c_est_le_tour):
        """Descendre dans l'arbre UCT"""
        # soit N la racine de l'arbre
        n = self.tree
        joueur = symbole_dont_c_est_le_tour
        # boucle : fils non explorés de N
        grille = Grille()
        grille.set(n.name)
        mes_coups_possibles = grille.look_for_allowed_steps()
        while all([(n.name, i) in self.compteur_choix_action_dans_etat for i in mes_coups_possibles]):
            # soit F le fils de N ayant la plus grande valeur UCT
            if len(mes_coups_possibles) > 0:
                action = self.choisir_action_uct(grille)
                nouvel_etat = changer_etat_apres_transition(n.name, action, joueur)
                f = Node(nouvel_etat, n)
                f.code = action
                n = f
                joueur = get_other_symbol(joueur)
                grille.set(n.name)
                mes_coups_possibles = grille.look_for_allowed_steps()
            else:
                break
        # soir F un fils de N tiré au hasard parmi les fils non explorés
        grille.set(n.name)
        mes_coups_possibles = grille.look_for_allowed_steps()
        if len(mes_coups_possibles) > 0:
            actions_inexplorees = [i for i in mes_coups_possibles if
                                   not ((n.name, i) in self.compteur_choix_action_dans_etat)]
            tirage = randint(0, len(actions_inexplorees) - 1)
            action = actions_inexplorees[tirage]
            etat_inexplore = changer_etat_apres_transition(n.name, action, joueur)
            f = Node(etat_inexplore, n)
            f.code = action
            joueur = get_other_symbol(joueur)
        else:
            f = n
        return f, joueur

    def tree_up(self, noeud__n, evaluation_r, symbole_racine, symbole_noeud_n):
        """Remonter dans l'arbre UCT"""
        symbole_courant = symbole_noeud_n
        while noeud__n is not self.tree:
            nom__n = noeud__n.name
            nom_parent__n = noeud__n.parent.name
            action_pour_arriver_en__n = noeud__n.code
            try:
                self.compteur_visite_etat[nom__n] += 1
            except KeyError:
                self.compteur_visite_etat[nom__n] = 1
            try:
                self.compteur_choix_action_dans_etat[(nom_parent__n, action_pour_arriver_en__n)] += 1
            except KeyError:
                self.compteur_choix_action_dans_etat[(nom_parent__n, action_pour_arriver_en__n)] = 1
            q = evaluation_r
            # Pour information, la ligne ci-dessous est juste, ne pas mettre de signe "!=" au lieu de "==".
            if symbole_courant == symbole_noeud_n:  # <- La ligne qui m'a fait perdre beaucoup de temps.
                q *= -1.0
            try:
                # En effet, nous nous intéressons au parent de N, et non à N lui-même.
                mu_avant = self.score_choix_action_dans_etat[(nom_parent__n, action_pour_arriver_en__n)]
            except KeyError:
                mu_avant = 0
            n = self.compteur_choix_action_dans_etat[(nom_parent__n, action_pour_arriver_en__n)]
            mu = mu_avant + (1.0 / n) * (q - mu_avant)
            self.score_choix_action_dans_etat[(nom_parent__n, action_pour_arriver_en__n)] = mu
            noeud__n = noeud__n.parent
            symbole_courant = get_other_symbol(symbole_courant)
        # Enfin, visite de la racine.
        try:
            self.compteur_visite_etat[noeud__n.name] += 1
        except KeyError:
            self.compteur_visite_etat[noeud__n.name] = 1
        return

    def choisir_action_uct(self, grille):
        """Choisir une action en utilisant le critère UCB"""
        etat = grille.get_name()
        mes_coups_possibles = grille.look_for_allowed_steps()
        meilleure_action = None
        meilleure_evaluation = None
        for action in mes_coups_possibles:
            if not ((etat, action) in self.score_choix_action_dans_etat):
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


def changer_etat_apres_transition(etat, action, joueur):
    """Déterminer l'état obtenu lorsque le joueur effectue l'action dans l'état donné"""
    grille_copiee = Grille()
    grille_copiee.set(etat)
    grille_copiee.drop(joueur, action)
    nouvel_etat = grille_copiee.get_name()
    return nouvel_etat
