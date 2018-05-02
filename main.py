# -*- coding: utf-8 -*-

# Source d'inspiration :
# http://www.cs.helsinki.fi/u/vpeltoni/

from time import sleep

from ai import AI
from grille import Grille
from mc import MC
from uct import UCT


def menu():
    """Menu principal"""
    # Intelligences artificielles disponibles :
    # 1 : jeu aléatoire biaisé
    # 2 : jeu Monte-Carlo biaisé
    # 3 : jeu UCT
    choix_ai_joueur = 3
    choix_ai_adversaire = 2
    num_tirages__m_c = 3
    num_descentes_dans_arbre = 7
    facteur_uct = 0.0
    num_parties_jouees = 50  # pour les statistiques de victoires
    user_input = []
    while user_input not in ['q']:
        user_input = input(
            "0) No player game.\n1) Single player game.\n2) Player vs player game.\n3) Statistiques.\nq) Quit.\nChoix : ")
        if user_input == '0':
            np(choix_ai_joueur, choix_ai_adversaire, num_tirages__m_c, num_descentes_dans_arbre, facteur_uct)
            print("\n\n")
        if user_input == '1':
            sp(choix_ai_adversaire, num_tirages__m_c, num_descentes_dans_arbre, facteur_uct)
            print("\n\n")
        if user_input == '2':
            pvp()
            print("\n\n")
        if user_input == '3':
            ratio_victoires = obtenir_statistiques_de_victoires(num_parties_jouees, choix_ai_joueur,
                                                                choix_ai_adversaire, num_tirages__m_c,
                                                                num_descentes_dans_arbre, facteur_uct)
            print("Choix AI du joueur 1 ?"),
            print(choix_ai_joueur)
            print("Choix AI du joueur 2 ?"),
            print(choix_ai_adversaire)
            if choix_ai_joueur != 1:
                print("Nombre de tirages MC ?"),
                print(num_tirages__m_c)
            if choix_ai_joueur == 3:
                print("Nombre de descentes dans l'arbre UCT ?"),
                print(num_descentes_dans_arbre)
                print("Facteur UCT ?"),
                print(facteur_uct)
            print("Pourcentage de victoires ?"),
            print(ratio_victoires)
            print("\n\n")


def np(choix_ai_joueur, choix_ai_adversaire, num_tirages_m_c=3, num_descentes_dans_arbre=7, facteur_uct=0.0,
       show_grid=False):
    """Une partie entre intelligences artificielles"""
    grid = Grille()
    ai1 = AI('X')
    if choix_ai_joueur == 2:
        ai1 = MC('X', num_tirages_m_c)
    elif choix_ai_joueur == 3:
        ai1 = UCT('X', num_tirages_m_c, num_descentes_dans_arbre, facteur_uct)
    ai2 = AI('O')
    if choix_ai_adversaire == 2:
        ai2 = MC('O')  # paramètres par défaut
    elif choix_ai_adversaire == 3:
        ai2 = UCT('O')  # paramètres par défaut
    le_joueur1_gagne = False
    mes_coups_possibles = grid.look_for_allowed_steps()
    while grid.check_victory() is False and len(mes_coups_possibles) > 0:
        mon_coup = ai1.ai(grid)
        grid.drop(ai1.player, mon_coup)
        le_joueur1_gagne = True
        mes_coups_possibles = grid.look_for_allowed_steps()
        if show_grid:
            grid.show_grid()
            sleep(1)
        if grid.check_victory() is False and len(mes_coups_possibles) > 0:
            votre_coup = ai2.ai(grid)
            grid.drop(ai2.player, votre_coup)
            le_joueur1_gagne = False
            mes_coups_possibles = grid.look_for_allowed_steps()
            if show_grid:
                grid.show_grid()
    il_y_a_un_vainqueur = grid.check_victory()
    print("The game ended in the following state:")
    grid.show_grid()
    print("Y a-t-il un gagnant ?"),
    print(il_y_a_un_vainqueur)
    print("Si oui, est-ce le joueur 1 (X) ?"),
    print(le_joueur1_gagne)
    return il_y_a_un_vainqueur, le_joueur1_gagne


def sp(choix_ai_adversaire, num_tirages_m_c=3, num_descentes_dans_arbre=7, facteur_uct=0.0):
    """Une partie opposant un joueur humain à une intelligence artificielle"""
    grid = Grille()
    ai = AI('O')
    if choix_ai_adversaire == 2:
        ai = MC('O', num_tirages_m_c)
    elif choix_ai_adversaire == 3:
        ai = UCT('O', num_tirages_m_c, num_descentes_dans_arbre, facteur_uct)
    le_joueur1_gagne = False
    mes_coups_possibles = grid.look_for_allowed_steps()
    user_input = []
    player = 'X'
    while user_input != 'q' and grid.check_victory() is False and len(mes_coups_possibles) > 0:
        grid.show_grid()
        user_input = input("Number 1 through 7  = drop disc, q = quit. \nYour move:")
        if user_input in ['1', '2', '3', '4', '5', '6', '7']:
            mon_coup = int(user_input)
            if grid.drop(player, mon_coup):
                le_joueur1_gagne = True
                mes_coups_possibles = grid.look_for_allowed_steps()
                if grid.check_victory() is False and len(mes_coups_possibles) > 0:
                    votre_coup = ai.ai(grid)
                    grid.drop(ai.player, votre_coup)
                    le_joueur1_gagne = False
                    mes_coups_possibles = grid.look_for_allowed_steps()
    il_y_a_un_vainqueur = grid.check_victory()
    print("The game ended in the following state:")
    grid.show_grid()
    print("Y a-t-il un gagnant ?"),
    print(il_y_a_un_vainqueur)
    print("Si oui, est-ce le joueur n 1 (X) ?"),
    print(le_joueur1_gagne)


def pvp():
    """Une partie entre joueurs humains"""
    grid = Grille()
    user_input = []
    player = 'X'
    while user_input != 'q' and grid.check_victory() is False:
        grid.show_grid()
        user_input = input("1 2 3 4 5 6 7  = drop disc, q = quit. \nPlayer " + player + " to move:")
        if user_input in ['1', '2', '3', '4', '5', '6', '7']:
            if grid.drop(player, int(user_input)):
                if player == 'X':
                    player = 'O'
                else:
                    player = 'X'
    print("The game ended in the following state:")
    grid.show_grid()


def obtenir_statistiques_de_victoires(num_parties_jouees, choix_ai_joueur, choix_ai_adversaire, num_tirages_m_c=3,
                                      num_descentes_dans_arbre=7, facteur_uct=0.0):
    num_parties_avec_vainqueur = 0
    num_victoires_du_joueur1 = 0
    for i in range(num_parties_jouees):
        (il_y_a_un_vainqueur, le_joueur1_gagne) = np(choix_ai_joueur, choix_ai_adversaire, num_tirages_m_c,
                                                     num_descentes_dans_arbre, facteur_uct)
        num_parties_avec_vainqueur += int(il_y_a_un_vainqueur)
        num_victoires_du_joueur1 += int(le_joueur1_gagne)
    try:
        ratio_victoires = round(100.0 * num_victoires_du_joueur1 / num_parties_avec_vainqueur) / 100.0
    except ZeroDivisionError:
        ratio_victoires = 0.5
    return ratio_victoires


if __name__ == "__main__":
    menu()
