# -*- coding: utf-8 -*-

# Source d'inspiration :
# http://www.cs.helsinki.fi/u/vpeltoni/

from random import randint

from win_conditions import look_for_obvious_steps


class AI:
    """Intelligence artificielle"""

    def __init__(self, symbole='O'):
        """Créer un joueur du symbole indiqué"""
        self.player = symbole
        pass

    def ai(self, grille):
        """Jouer de façon aléatoire biaisée : un coups urgent sous réserve d'existence,
        sinon un coup possible au hasard"""
        mon_coup_urgent = look_for_obvious_steps(grille)
        if mon_coup_urgent == -1:
            mes_coups_possibles = grille.look_for_allowed_steps()
            tirage_aleatoire = randint(0, len(mes_coups_possibles) - 1)
            return mes_coups_possibles[tirage_aleatoire]
        else:
            return mon_coup_urgent

    def auto_complete(self, grille):
        """Simuler une fin de partie à partir de la grille initiale fournie :
        méthode Monte-Carlo avec un jeu aléatoire biaisé pour les joueurs"""
        adversaire = 'X'
        if self.player == 'X':
            adversaire = 'O'
        le_joueur1_gagne = False
        mes_coups_possibles = grille.look_for_allowed_steps()
        while grille.check_victory() is False and len(mes_coups_possibles) > 0:
            mon_coup = self.ai(grille)
            grille.drop(self.player, mon_coup)
            le_joueur1_gagne = True
            mes_coups_possibles = grille.look_for_allowed_steps()
            if grille.check_victory() is False and len(mes_coups_possibles) > 0:
                votre_coup = self.ai(grille)
                grille.drop(adversaire, votre_coup)
                le_joueur1_gagne = False
                mes_coups_possibles = grille.look_for_allowed_steps()
        il_y_a_un_vainqueur = grille.check_victory()
        return il_y_a_un_vainqueur, le_joueur1_gagne
