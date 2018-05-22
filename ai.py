from win_conditions import look_for_obvious_steps


class AI:
    """Intelligence artificielle"""

    def __init__(self, symbole='O'):
        """Créer un joueur du symbole indiqué"""
        self.player = symbole

    def play_witout_bias(self, grille):
        """Jouer de façon non biaisée : renvoyer au hasard un coup possible"""
        return grille.get_random_allowed_step()

    def play_with_bias(self, grille):
        """Jouer de façon biaisée : vérifier s'il est possible de gagner en un coup avant toute réflexion"""
        mon_coup_urgent = look_for_obvious_steps(grille)
        if mon_coup_urgent is None:
            return self.play_witout_bias(grille)
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
            mon_coup = self.play_with_bias(grille)
            grille.drop(self.player, mon_coup)
            le_joueur1_gagne = True
            mes_coups_possibles = grille.look_for_allowed_steps()
            if grille.check_victory() is False and len(mes_coups_possibles) > 0:
                votre_coup = self.play_with_bias(grille)
                grille.drop(adversaire, votre_coup)
                le_joueur1_gagne = False
                mes_coups_possibles = grille.look_for_allowed_steps()
        il_y_a_un_vainqueur = grille.check_victory()
        return il_y_a_un_vainqueur, le_joueur1_gagne
