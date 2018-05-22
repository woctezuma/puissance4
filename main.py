from time import sleep

from ai import AI
from grille import Grille
from mc import MC
from uct import UCT


def get_conversion_offset():
    return 97


def get_possible_player_inputs(width):
    return [chr(i + get_conversion_offset()) for i in range(width)]


def convert_player_input(player_input):
    return ord(player_input) - get_conversion_offset() + 1


def menu(default_user_action=None):
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
        if default_user_action is not None:
            user_input = default_user_action
        else:
            user_input = input(
                "0) No player game.\n" +
                "1) Single player game.\n" +
                "2) Player vs player game.\n" +
                "3) Statistiques.\n" +
                "q) Quit.\n" +
                "Choix : ")

        if user_input == '0':
            np(choix_ai_joueur, choix_ai_adversaire, num_tirages__m_c, num_descentes_dans_arbre, facteur_uct)
        if user_input == '1':
            sp(choix_ai_adversaire, num_tirages__m_c, num_descentes_dans_arbre, facteur_uct)
        if user_input == '2':
            pvp()
        if user_input == '3':
            ratio_victoires = obtenir_statistiques_de_victoires(num_parties_jouees, choix_ai_joueur,
                                                                choix_ai_adversaire, num_tirages__m_c,
                                                                num_descentes_dans_arbre, facteur_uct)
            print("[Player #1] AI = {}".format(choix_ai_joueur))
            print("[Player #2] AI = {}".format(choix_ai_adversaire))
            if choix_ai_joueur != 1:
                print("[Monte Carlo] num_samples = {}".format(num_tirages__m_c))
            if choix_ai_joueur == 3:
                print("[Upper Confidence Tree] num_tree_descents = {}".format(num_descentes_dans_arbre))
                print("[Upper Confidence Tree] factor = {}".format(facteur_uct))
            print("[Player #1 vs. Player #2] winrate = {:.2f}".format(ratio_victoires))
        if default_user_action is not None:
            user_input = 'q'
        print("\n\n")

    return True


def np(choix_ai_joueur, choix_ai_adversaire, num_tirages_m_c=3, num_descentes_dans_arbre=7, facteur_uct=0.0,
       show_grid=False, verbose=True):
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
        mon_coup = ai1.play_with_bias(grid)
        grid.drop(ai1.player, mon_coup)
        le_joueur1_gagne = True
        mes_coups_possibles = grid.look_for_allowed_steps()
        if show_grid:
            grid.show_grid()
            sleep(1)
        if grid.check_victory() is False and len(mes_coups_possibles) > 0:
            votre_coup = ai2.play_with_bias(grid)
            grid.drop(ai2.player, votre_coup)
            le_joueur1_gagne = False
            mes_coups_possibles = grid.look_for_allowed_steps()
            if show_grid:
                grid.show_grid()
    il_y_a_un_vainqueur = grid.check_victory()
    if verbose:
        print("The game ended in the following state:")
        grid.show_grid()
        print("Y a-t-il un gagnant ? {}".format(il_y_a_un_vainqueur))
        print("Si oui, est-ce le joueur 1 (X) ? {}".format(le_joueur1_gagne))
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
        user_input = input("Letter a through g  = drop disc, q = quit. \nYour move:")
        if user_input in get_possible_player_inputs(grid.width):
            mon_coup = convert_player_input(user_input)
            if grid.drop(player, mon_coup):
                le_joueur1_gagne = True
                mes_coups_possibles = grid.look_for_allowed_steps()
                if grid.check_victory() is False and len(mes_coups_possibles) > 0:
                    votre_coup = ai.play_with_bias(grid)
                    grid.drop(ai.player, votre_coup)
                    le_joueur1_gagne = False
                    mes_coups_possibles = grid.look_for_allowed_steps()
    il_y_a_un_vainqueur = grid.check_victory()
    print("The game ended in the following state:")
    grid.show_grid()
    print("Y a-t-il un gagnant ? {}".format(il_y_a_un_vainqueur))
    print("Si oui, est-ce le joueur 1 (X) ? {}".format(le_joueur1_gagne))
    return


def pvp():
    """Une partie entre joueurs humains"""
    grid = Grille()
    user_input = []
    player = 'X'
    while user_input != 'q' and grid.check_victory() is False:
        grid.show_grid()
        user_input = input("Letter a through g = drop disc, q = quit. \nPlayer " + player + " to move:")
        if user_input in get_possible_player_inputs(grid.width):
            mon_coup = convert_player_input(user_input)
            if grid.drop(player, mon_coup):
                if player == 'X':
                    player = 'O'
                else:
                    player = 'X'
    print("The game ended in the following state:")
    grid.show_grid()
    return


def obtenir_statistiques_de_victoires(num_parties_jouees, choix_ai_joueur, choix_ai_adversaire, num_tirages_m_c=3,
                                      num_descentes_dans_arbre=7, facteur_uct=0.0):
    num_parties_avec_vainqueur = 0
    num_victoires_du_joueur1 = 0
    for game_no in range(num_parties_jouees):
        print('Game n°{}'.format(game_no + 1))
        (il_y_a_un_vainqueur, le_joueur1_gagne) = np(choix_ai_joueur, choix_ai_adversaire, num_tirages_m_c,
                                                     num_descentes_dans_arbre, facteur_uct, verbose=False)
        num_parties_avec_vainqueur += int(il_y_a_un_vainqueur)
        num_victoires_du_joueur1 += int(le_joueur1_gagne)
    try:
        ratio_victoires = num_victoires_du_joueur1 / num_parties_avec_vainqueur
    except ZeroDivisionError:
        ratio_victoires = 0.5
    return ratio_victoires


if __name__ == "__main__":
    test_user_action = '0'
    # Set to None if you want to decide at run-time which kind of play you prefer (AI self-play, human vs. AI, etc.)
    # Set to '0' to let AI vs. AI self-play (useful for Travis integration on Github)
    # Set to '1' to play one game against biased Monte-Carlo AI.
    # NB: This should not be the best AI. Modify the code if you want to play against UCT AI.
    # Set to '2' to allow with no AI, i.e. human vs. human.
    # Set to '3' to compute AI self-play 50 games: UCT AI vs. biased Monte-Carlo AI.

    menu(test_user_action)
