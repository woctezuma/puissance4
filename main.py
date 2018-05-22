from time import sleep

from grille import Grille
from mc import MC
from uct import UCT
from utils import get_possible_player_inputs, convert_player_input


def menu(default_user_action=None):
    """Menu principal"""
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
            player_X = UCT('X')
            player_X.set_params(player_X.get_default_params())

            player_O = MC('O')
            player_O.set_params(player_O.get_default_params())

            np(player_X, player_O)

            player_X.print()
            player_O.print()

        if user_input == '1':
            player_O = UCT('O')
            player_O.set_params(player_O.get_default_params())

            sp(player_O)

        if user_input == '2':
            pvp()

        if user_input == '3':
            player_X = UCT('X')
            player_X.set_params(player_X.get_default_params())

            player_O = MC('O')
            player_O.set_params(player_O.get_default_params())

            num_parties_jouees = 50

            ratio_victoires = obtenir_statistiques_de_victoires(player_X, player_O, num_parties_jouees)

            print("[Players X vs. O] winrate = {:.2f} (over {} games)".format(ratio_victoires, num_parties_jouees))

            player_X.print()
            player_O.print()

        if default_user_action is not None:
            user_input = 'q'

    return True


def np(player_X, player_O, show_grid=False, verbose=True):
    """Une partie entre intelligences artificielles"""
    grid = Grille()

    # TODO

    le_joueur1_gagne = False
    mes_coups_possibles = grid.look_for_allowed_steps()
    while grid.check_victory() is False and len(mes_coups_possibles) > 0:
        mon_coup = player_X.play_with_bias(grid)
        grid.drop(player_X.player, mon_coup)
        le_joueur1_gagne = True
        mes_coups_possibles = grid.look_for_allowed_steps()
        if show_grid:
            grid.show_grid()
            sleep(1)
        if grid.check_victory() is False and len(mes_coups_possibles) > 0:
            votre_coup = player_O.play_with_bias(grid)
            grid.drop(player_O.player, votre_coup)
            le_joueur1_gagne = False
            mes_coups_possibles = grid.look_for_allowed_steps()
            if show_grid:
                grid.show_grid()
    il_y_a_un_vainqueur = grid.check_victory()
    num_steps = grid.get_num_steps()

    if verbose:
        print_victory_screen(grid)

    return il_y_a_un_vainqueur, le_joueur1_gagne, num_steps


def sp(player_O):
    """Une partie opposant un joueur humain à une intelligence artificielle"""
    grid = Grille()

    # TODO

    mes_coups_possibles = grid.look_for_allowed_steps()
    user_input = []
    player = 'X'
    while user_input != 'q' and grid.check_victory() is False and len(mes_coups_possibles) > 0:
        grid.show_grid()
        user_input = input("Letter a through g  = drop disc, q = quit. \nYour move:")
        if user_input in get_possible_player_inputs(grid.width):
            mon_coup = convert_player_input(user_input)
            if grid.drop(player, mon_coup):

                mes_coups_possibles = grid.look_for_allowed_steps()
                if grid.check_victory() is False and len(mes_coups_possibles) > 0:
                    votre_coup = player_O.play_with_bias(grid)
                    grid.drop(player_O.player, votre_coup)

                    mes_coups_possibles = grid.look_for_allowed_steps()

    print_victory_screen(grid)
    return


def pvp():
    """Une partie entre joueurs humains"""
    grid = Grille()
    user_input = []
    player = 'X'
    last_player = None
    while user_input != 'q' and not (grid.check_victory()):
        grid.show_grid()
        user_input = input("Letter a through g = drop disc, q = quit. \nPlayer " + player + " to move:")
        if user_input in get_possible_player_inputs(grid.width):
            mon_coup = convert_player_input(user_input)
            last_player = player
            if grid.drop(player, mon_coup):
                if player == 'X':
                    player = 'O'
                else:
                    player = 'X'
    print_victory_screen(grid, last_player)
    return


def print_victory_screen(grid, winner_symbol='draw'):
    grid.show_grid()

    if winner_symbol is not None:
        if winner_symbol != 'draw':
            print("Player {} wins. ".format(winner_symbol))
        else:
            print("This is a draw. ".format(winner_symbol))

    return


def obtenir_statistiques_de_victoires(player_X, player_O, num_parties_jouees):
    # TODO

    num_parties_avec_vainqueur = 0
    num_victoires_du_joueur1 = 0
    for game_no in range(num_parties_jouees):
        (il_y_a_un_vainqueur, le_joueur1_gagne, num_steps) = np(player_X, player_O, verbose=False)
        num_parties_avec_vainqueur += int(il_y_a_un_vainqueur)
        num_victoires_du_joueur1 += int(le_joueur1_gagne)
        print('Game n°{}\tnum_steps={}'.format(game_no + 1, num_steps))
    try:
        ratio_victoires = num_victoires_du_joueur1 / num_parties_avec_vainqueur
    except ZeroDivisionError:
        ratio_victoires = 0.5
    return ratio_victoires


if __name__ == "__main__":
    test_user_action = '3'
    # Set to None if you want to decide at run-time which kind of play you prefer (AI self-play, human vs. AI, etc.)
    # Set to '0' to let AI vs. AI self-play (useful for Travis integration on Github)
    # Set to '1' to play one game against biased Monte-Carlo AI.
    # NB: This should not be the best AI. Modify the code if you want to play against UCT AI.
    # Set to '2' to allow with no AI, i.e. human vs. human.
    # Set to '3' to compute AI self-play 50 games: UCT AI vs. biased Monte-Carlo AI.

    menu(test_user_action)
