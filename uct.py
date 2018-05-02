# -*- coding: utf-8 -*-

from math import sqrt, log
from random import randint

from grille import Grille
from mc import MC, get_other_symbol
from node import Node


# Articles de référence :
# [1] T. Cazenave, A. Saffidine,
#     Utilisation de la recherche arborescente Monte-Carlo au Hex,
#     Revue d'Intelligence Artificielle, vol. 23, no. 2-3, pp. 183-202, 2009.
# [2] F. Teytaud, O. Teytaud,
#     Creating an Upper-Condence-Tree program for Havannah,
#     Advances in Computer Games 12, in Pamplona, Spain, 2009.

class UCT(MC):
    """Intelligence artificielle reposant sur l'algorithme Upper-Confidence-Tree"""

    def __init__(self, symbole='O', num_tirages_m_c=3, num_descentes_dans_arbre=7, facteur_uct=0.0):
        """Créer un joueur du symbole indiqué"""
        MC.__init__(self, symbole, num_tirages_m_c)
        self.num_descentes_dans_arbre = num_descentes_dans_arbre
        self.facteur_uct = facteur_uct

    def ai_uct(self, grille):
        """Déterminer la meilleure action en fonction des résultats de l'exploration UCT"""
        # recevoir une position p
        etat_initial = grille.get_name()
        symbole_dont_c_est_le_tour = self.player
        # soit A l'arbre UCT vide à la racine près
        self.tree = Node(etat_initial)
        self.compteur_visite_etat = {}
        self.score_choix_action_dans_etat = {}
        self.compteur_choix_action_dans_etat = {}
        # boucle : plusieurs descentes dans l'arbre
        for i in range(self.num_descentes_dans_arbre):
            # soit p' une copie de p
            grille_copiee = Grille()
            grille_copiee.set(etat_initial)
            # soit N le noeud résultat d'une descente dans l'arbre (A, p')
            (N, symbole_dont_c_est_le_tour_pour_N) = self.TreeDown(grille_copiee, symbole_dont_c_est_le_tour)
            # soit R l'évaluation de p'
            grille_pour__n = N.name
            grille_simulee = Grille()
            grille_simulee.set(grille_pour__n)
            R = self.simuler_monte_carlo(grille_simulee, symbole_dont_c_est_le_tour_pour_N)
            # nous effectuons une remontée de l'arbre (A, N, R)
            self.TreeUp(N, R, symbole_dont_c_est_le_tour, symbole_dont_c_est_le_tour_pour_N)
        # renvoyer le coup fils (de la racine de A) qui a la meilleure valeur UCT
        meilleure_action = self.choisir_action_uct(grille)
        return meilleure_action

    def ai(self, grille):
        """Jouer en fonction des résultats de l'exploration UCT"""
        mon_coup_urgent = self.look_for_obvious_steps(grille)
        if mon_coup_urgent == -1:
            mon_coup = self.ai_uct(grille)
            return mon_coup
        else:
            return mon_coup_urgent

    def TreeDown(self, position_courante, symbole_dont_c_est_le_tour):
        """Descendre dans l'arbre UCT"""
        # soit N la racine de l'arbre
        N = self.tree
        joueur = symbole_dont_c_est_le_tour
        # boucle : fils non explorés de N
        grille = Grille()
        grille.set(N.name)
        mes_coups_possibles = grille.look_for_allowed_steps()
        while all([(N.name, i) in self.compteur_choix_action_dans_etat for i in mes_coups_possibles]):
            # soit F le fils de N ayant la plus grande valeur UCT
            if len(mes_coups_possibles) > 0:
                action = self.choisir_action_uct(grille)
                nouvel_etat = changerEtatApresTransition(N.name, action, joueur)
                F = Node(nouvel_etat, N)
                F.code = action
                N = F
                joueur = get_other_symbol(joueur)
                grille.set(N.name)
                mes_coups_possibles = grille.look_for_allowed_steps()
            else:
                break
        # soir F un fils de N tiré au hasard parmi les fils non explorés
        grille.set(N.name)
        mes_coups_possibles = grille.look_for_allowed_steps()
        if len(mes_coups_possibles) > 0:
            actions_inexplorees = [i for i in mes_coups_possibles if
                                   not ((N.name, i) in self.compteur_choix_action_dans_etat)]
            tirage = randint(0, len(actions_inexplorees) - 1)
            action = actions_inexplorees[tirage]
            etat_inexplore = changerEtatApresTransition(N.name, action, joueur)
            F = Node(etat_inexplore, N)
            F.code = action
            joueur = get_other_symbol(joueur)
        else:
            F = N
        return F, joueur

    def TreeUp(self, noeud__n, evaluation_R, symbole_racine, symbole_noeud_N):
        """Remonter dans l'arbre UCT"""
        symbole_courant = symbole_noeud_N
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
            q = evaluation_R
            # Pour information, la ligne ci-dessous est juste, ne pas mettre de signe "!=" au lieu de "==".
            if symbole_courant == symbole_noeud_N:  # <- La ligne qui m'a fait perdre beaucoup de temps.
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
            if evaluation > meilleure_evaluation:
                meilleure_evaluation = evaluation
                meilleure_action = action
        if meilleure_action is None:
            print("Aucun coup admissible.")
        return meilleure_action


def changerEtatApresTransition(etat, action, joueur):
    """Déterminer l'état obtenu lorsque le joueur effectue l'action dans l'état donné"""
    grille_copiee = Grille()
    grille_copiee.set(etat)
    grille_copiee.drop(joueur, action)
    nouvel_etat = grille_copiee.get_name()
    return nouvel_etat
