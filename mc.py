# -*- coding: utf-8 -*-

from ai import AI
from grille import Grille

class MC(AI):
    """Intelligence artificielle reposant sur des simulations Monte-Carlo"""

    def __init__(self, symbole = 'O', num_tirages_MC = 3):
        """Créer un joueur du symbole indiqué"""
        AI.__init__(self, symbole)
        self.num_tirages_MC = num_tirages_MC

    def simulerMonteCarlo(self, grille, symbole_dont_c_est_le_tour):
        """Evaluer une grille par des simulations Monte-Carlo de la fin de la partie"""
        ai = AI(symbole_dont_c_est_le_tour)
        num_parties_avec_vainqueur = 0
        num_victoires_du_joueur1 = 0
        for i in range(self.num_tirages_MC):
            grille_simulee = Grille(grille)
            (il_y_a_un_vainqueur, le_joueur1_gagne) = ai.autoComplete(grille_simulee)
            num_parties_avec_vainqueur += int(il_y_a_un_vainqueur)
            num_victoires_du_joueur1 += int(le_joueur1_gagne)
        try:
            score  = (2.0*num_victoires_du_joueur1 - num_parties_avec_vainqueur)/num_parties_avec_vainqueur
        except ZeroDivisionError:
            score = 0.5
        return score

    def aiMonteCarlo(self, grille):
        """Déterminer la meilleure action en fonction des résultats des simulations Monte-Carlo"""
        mes_coups_possibles = grille.lookForAllowedSteps()
        meilleure_action = None
        meilleure_evaluation = None
        for action in mes_coups_possibles:
            grille_simulee = Grille(grille)
            # Le joueur (A) joue un coup.
            grille_simulee.drop(self.player, action)
            # C'est au tour de l'autre joueur (B).
            symbole_dont_c_est_le_tour = getOtherSymbol(self.player)
            # Nous prenons l'opposé de la valeur simulée, car nous nous intéressons au joueur A.
            evaluation = - self.simulerMonteCarlo(grille_simulee, symbole_dont_c_est_le_tour)
            if evaluation > meilleure_evaluation:
                    meilleure_evaluation = evaluation
                    meilleure_action = action
        return meilleure_action

    def ai(self, grille):
        """Jouer en fonction des résultats des simulations Monte-Carlo"""
        mon_coup_urgent = self.lookForObviousSteps(grille)
        if mon_coup_urgent == -1:
                mon_coup = self.aiMonteCarlo(grille)
                return mon_coup
        else:
                return mon_coup_urgent

def getOtherSymbol(symbole):
    """Passer du symbole d'un joueur au symbole de son adversaire"""
    if symbole == 'X':
            return 'O'
    else:
            return 'X'
