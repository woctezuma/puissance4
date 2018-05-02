# -*- coding: utf-8 -*-

# Source d'inspiration :
# http://www.cs.helsinki.fi/u/vpeltoni/

from random import randint


class AI:
    """Intelligence artificielle"""

    def __init__(self, symbole='O'):
        """Créer un joueur du symbole indiqué"""
        self.player = symbole
        pass

    def look_for_obvious_steps(self, grille):
        """Vérifier s'il est possible de gagner pour l'un ou l'autre joueur.
        Si oui, renvoyer le numéro de la colonne à jouer, sinon -1"""
        for y in range(0, len(grille.grid)):
            for x in range(0, len(grille.grid[y])):
                '''Rechercher un coup qui permette ou empêche un alignement de quatre jetons'''
                if grille.grid[y][x] != '.':
                    '''Alignement horizontal de trois jetons consécutifs, le noeud (x,y) étant le plus à gauche'''
                    if x < grille.width - 3:
                        if grille.grid[y][x] == grille.grid[y][x + 1] and grille.grid[y][x] == grille.grid[y][x + 2]:
                            if y < grille.heigth - 1:
                                if grille.grid[y + 1][x + 3] != '.' and grille.grid[y][x + 3] == '.':
                                    return x + 4
                            elif grille.grid[y][x + 3] == '.':
                                return x + 4
                    '''Alignement vertical de trois jetons consécutifs, le noeud (x,y) étant le plus haut'''
                    if grille.heigth - 2 > y >= 1:
                        if grille.grid[y][x] == grille.grid[y + 1][x] and grille.grid[y][x] == grille.grid[y + 2][x]:
                            if grille.grid[y - 1][x] == '.':
                                return x + 1
                    '''Alignement horizontal de trois jetons consécutifs, le noeud (x,y) étant le plus à droite'''
                    if x > 2:
                        if grille.grid[y][x] == grille.grid[y][x - 1] and grille.grid[y][x] == grille.grid[y][x - 2]:
                            if y < grille.heigth - 1:
                                if grille.grid[y + 1][x - 3] != '.' and grille.grid[y][x - 3] == '.':
                                    return x - 2
                            elif grille.grid[y][x - 3] == '.':
                                return x - 2
                    '''Alignement horizontal de trois jetons non consécutifs, le noeud (x,y) étant le plus à gauche'''
                    if x < grille.width - 3:
                        if grille.grid[y][x] == grille.grid[y][x + 3]:
                            '''Alignement horizontal de la forme X.XX'''
                            if grille.grid[y][x] == grille.grid[y][x + 2]:
                                if y < grille.heigth - 1:
                                    if grille.grid[y + 1][x + 1] != '.' and grille.grid[y][x + 1] == '.':
                                        return x + 2
                                elif grille.grid[y][x + 1] == '.':
                                    return x + 2
                            '''Alignement horizontal de la forme XX.X'''
                            if grille.grid[y][x] == grille.grid[y][x + 1]:
                                if y < grille.heigth - 1:
                                    if grille.grid[y + 1][x + 2] != '.' and grille.grid[y][x + 2] == '.':
                                        return x + 3
                                elif grille.grid[y][x + 2] == '.':
                                    return x + 3
                    '''Alignement diagonal descendant : allant du coin haut gauche au coin bas droit'''
                    if y < grille.heigth - 3 and x < grille.width - 3:
                        if grille.grid[y][x] == grille.grid[y + 3][x + 3]:
                            '''Alignement diagonal de la forme X.XX'''
                            if grille.grid[y][x] == grille.grid[y + 2][x + 2]:
                                if grille.grid[y + 2][x + 1] != '.' and grille.grid[y + 1][x + 1] == '.':
                                    return x + 2
                            '''Alignement diagonal de la forme XX.X'''
                            if grille.grid[y][x] == grille.grid[y + 1][x + 1]:
                                if grille.grid[y + 3][x + 2] != '.' and grille.grid[y + 2][x + 2] == '.':
                                    return x + 3
                        '''Alignement diagonal, le noeud (x,y) étant le plus haut et à gauche'''
                        if grille.grid[y][x] == grille.grid[y + 1][x + 1] and \
                                grille.grid[y][x] == grille.grid[y + 2][x + 2]:
                            if y < grille.heigth - 4:
                                if grille.grid[y + 4][x + 3] != '.' and grille.grid[y + 3][x + 3] == '.':
                                    return x + 4
                            elif grille.grid[y + 3][x + 3] == '.':
                                return x + 4
                    '''Alignement diagonal montant : allant du coin bas gauche au coin haut droit'''
                    if y < grille.heigth - 3 and x > 2:
                        if grille.grid[y][x] == grille.grid[y + 3][x - 3]:
                            '''Alignement diagonal de la forme X.XX'''
                            if grille.grid[y][x] == grille.grid[y + 2][x - 2]:
                                if grille.grid[y + 2][x - 1] != '.' and grille.grid[y + 1][x - 1] == '.':
                                    return x
                            '''Alignement diagonal de la forme XX.X'''
                            if grille.grid[y][x] == grille.grid[y + 1][x - 1]:
                                if grille.grid[y + 3][x - 2] != '.' and grille.grid[y + 2][x - 2] == '.':
                                    return x - 1
                        '''Alignement diagonal, le noeud (x,y) étant le plus haut et à droite'''
                        if grille.grid[y][x] == grille.grid[y + 1][x - 1] and \
                                grille.grid[y][x] == grille.grid[y + 2][x - 2]:
                            if y < grille.heigth - 4:
                                if grille.grid[y + 4][x - 3] != '.' and grille.grid[y + 3][x - 3] == '.':
                                    return x - 2
                            elif grille.grid[y + 3][x - 3] == '.':
                                return x - 2
                    '''Alignement diagonal montant de la forme XXX., le noeud (x,y) étant le plus bas et à gauche'''
                    if y > 3 and x < grille.width - 3:
                        if grille.grid[y][x] == grille.grid[y - 1][x + 1] \
                                and grille.grid[y][x] == grille.grid[y - 2][x + 2]:
                            if grille.grid[y - 2][x + 3] != '.' and grille.grid[y - 3][x + 3] == '.':
                                return x + 4
                    '''Alignement diagonal descendant de la forme .XXX, le noeud (x,y) étant le plus bas et à droite'''
                    if y > 3 and x > 2:
                        if grille.grid[y][x] == grille.grid[y - 1][x - 1] \
                                and grille.grid[y][x] == grille.grid[y - 2][x - 2]:
                            if grille.grid[y - 2][x - 3] != '.' and grille.grid[y - 3][x - 3] == '.':
                                return x - 2
        '''Aucun coup urgent, alors renvoyer -1'''
        return -1

    def ai(self, grille):
        """Jouer de façon aléatoire biaisée : un coups urgent sous réserve d'existence,
        sinon un coup possible au hasard"""
        mon_coup_urgent = self.look_for_obvious_steps(grille)
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
