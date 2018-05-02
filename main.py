# -*- coding: utf-8 -*-

# Source d'inspiration :
# http://www.cs.helsinki.fi/u/vpeltoni/

from time import sleep
from ai import AI
from mc import MC
from uct import UCT
from grille import Grille

def menu():
    """Menu principal"""
    # Intelligences artificielles disponibles :
    # 1 : jeu aléatoire biaisé
    # 2 : jeu Monte-Carlo biaisé
    # 3 : jeu UCT
    choix_ai_joueur = 3
    choix_ai_adversaire = 2
    num_tirages_MC = 3
    num_descentes_dans_arbre = 7
    facteur_uct = 0.0
    num_parties_jouees = 50 # pour les statistiques de victoires
    input = []
    while input not in ['q']:
        input = raw_input("0) No player game.\n1) Single player game.\n2) Player vs player game.\n3) Statistiques.\nq) Quit.\nChoix : ")
        if input == '0':
            np(choix_ai_joueur, choix_ai_adversaire, num_tirages_MC, num_descentes_dans_arbre, facteur_uct)
            print("\n\n")
        if input == '1':
            sp(choix_ai_adversaire, num_tirages_MC, num_descentes_dans_arbre, facteur_uct)
            print("\n\n")
        if input == '2':
            pvp()
            print("\n\n")
        if input == '3':
            ratio_victoires = obtenirStatistiquesDeVictoires(num_parties_jouees, choix_ai_joueur, choix_ai_adversaire, num_tirages_MC, num_descentes_dans_arbre, facteur_uct)
            print("Choix AI du joueur 1 ?"),
            print(choix_ai_joueur)
            print("Choix AI du joueur 2 ?"),
            print(choix_ai_adversaire)
            if choix_ai_joueur != 1:
                print("Nombre de tirages MC ?"),
                print(num_tirages_MC)
            if choix_ai_joueur == 3:
                print("Nombre de descentes dans l'arbre UCT ?"),
                print(num_descentes_dans_arbre)
                print("Facteur UCT ?"),
                print(facteur_uct)
            print("Pourcentage de victoires ?"),
            print(ratio_victoires)
            print("\n\n")

def np(choix_ai_joueur, choix_ai_adversaire, num_tirages_MC = 3, num_descentes_dans_arbre = 7, facteur_uct = 0.0, show_grid = False):
    """Une partie entre intelligences artificielles"""
    grid = Grille()
    ai1 = AI('X')
    if choix_ai_joueur == 2:
        ai1 = MC('X', num_tirages_MC)
    elif choix_ai_joueur == 3:
        ai1 = UCT('X', num_tirages_MC, num_descentes_dans_arbre, facteur_uct)
    ai2 = AI('O')
    if choix_ai_adversaire == 2:
        ai2 = MC('O') # paramètres par défaut
    elif choix_ai_adversaire == 3:
        ai2 = UCT('O') # paramètres par défaut
    le_joueur1_gagne = False
    mes_coups_possibles = grid.lookForAllowedSteps()
    while grid.checkVictory() is False and len(mes_coups_possibles)>0:
        MonCoup = ai1.ai(grid)
        grid.drop(ai1.player, MonCoup)
        le_joueur1_gagne = True
        mes_coups_possibles = grid.lookForAllowedSteps()
        if show_grid:
            grid.showGrid()
            sleep(1)
        if grid.checkVictory() is False and len(mes_coups_possibles)>0:
            VotreCoup = ai2.ai(grid)
            grid.drop(ai2.player, VotreCoup)
            le_joueur1_gagne = False
            mes_coups_possibles = grid.lookForAllowedSteps()
            if show_grid:
                grid.showGrid()
    il_y_a_un_vainqueur = grid.checkVictory()
    print("The game ended in the following state:")
    grid.showGrid()
    print("Y a-t-il un gagnant ?"),
    print(il_y_a_un_vainqueur)
    print("Si oui, est-ce le joueur 1 (X) ?"),
    print(le_joueur1_gagne)
    return il_y_a_un_vainqueur, le_joueur1_gagne

def sp(choix_ai_adversaire, num_tirages_MC = 3, num_descentes_dans_arbre = 7, facteur_uct = 0.0):
    """Une partie opposant un joueur humain à une intelligence artificielle"""
    grid = Grille()
    ai = AI('O')
    if choix_ai_adversaire == 2:
        ai = MC('O', num_tirages_MC)
    elif choix_ai_adversaire == 3:
        ai = UCT('O', num_tirages_MC, num_descentes_dans_arbre, facteur_uct)
    le_joueur1_gagne = False
    mes_coups_possibles = grid.lookForAllowedSteps()
    input = []
    player = 'X'
    while input != 'q' and grid.checkVictory() is False and len(mes_coups_possibles)>0:
        grid.showGrid()
        input = raw_input("Number 1 through 7  = drop disc, q = quit. \nYour move:")
        if input in ['1', '2', '3', '4', '5', '6', '7']:
            MonCoup = int(input)
            if grid.drop(player, MonCoup):
                le_joueur1_gagne = True
                mes_coups_possibles = grid.lookForAllowedSteps()
                if grid.checkVictory() is False and len(mes_coups_possibles)>0:
                    VotreCoup = ai.ai(grid)
                    grid.drop(ai.player, VotreCoup)
                    le_joueur1_gagne = False
                    mes_coups_possibles = grid.lookForAllowedSteps()
    il_y_a_un_vainqueur = grid.checkVictory()
    print("The game ended in the following state:")
    grid.showGrid()
    print("Y a-t-il un gagnant ?"),
    print(il_y_a_un_vainqueur)
    print("Si oui, est-ce le joueur n 1 (X) ?"),
    print(le_joueur1_gagne)

def pvp():
    """Une partie entre joueurs humains"""
    grid = Grille()
    input = []
    player = 'X'
    while input != 'q' and grid.checkVictory() is False:
        grid.showGrid()
        input = raw_input("1 2 3 4 5 6 7  = drop disc, q = quit. \nPlayer " +player+" to move:")
        if input in ['1', '2', '3', '4', '5', '6', '7']:
            if grid.drop(player, int(input)):
                if player == 'X':
                    player = 'O'
                else:
                    player = 'X'
    print("The game ended in the following state:")
    grid.showGrid()

def obtenirStatistiquesDeVictoires(num_parties_jouees, choix_ai_joueur, choix_ai_adversaire, num_tirages_MC = 3, num_descentes_dans_arbre = 7, facteur_uct = 0.0):
    num_parties_avec_vainqueur = 0
    num_victoires_du_joueur1 = 0
    for i in range(num_parties_jouees):
        (il_y_a_un_vainqueur, le_joueur1_gagne) = np(choix_ai_joueur, choix_ai_adversaire, num_tirages_MC, num_descentes_dans_arbre, facteur_uct)
        num_parties_avec_vainqueur += int(il_y_a_un_vainqueur)
        num_victoires_du_joueur1 += int(le_joueur1_gagne)
    try:
        ratio_victoires = round(100.0*num_victoires_du_joueur1/num_parties_avec_vainqueur)/100.0
    except ZeroDivisionError:
        ratio_victoires = 0.5
    return ratio_victoires

if __name__ == "__main__":
    menu()
