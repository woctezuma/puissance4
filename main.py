from grille import Grille
from mc import MC
from uct import UCT
from utils import get_possible_player_inputs, convert_player_input


def menu(default_user_action=None, num_parties_jouees=50):
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

            ratio_victoires = analyze_AI_self_plays(player_X, player_O, num_parties_jouees)

            print("\n[Players X vs. O] winrate = {:.2f} (over {} games)".format(ratio_victoires, num_parties_jouees))

            player_X.print()
            player_O.print()

        if default_user_action is not None:
            user_input = 'q'

    return True


def np(ai_player_X, ai_player_O, verbose=True):
    """Une partie entre intelligences artificielles"""
    grille = Grille()
    player_who_last_played = None

    step_counter = 0
    while not (grille.check_victory()) and len(grille.look_for_allowed_steps()) > 0:

        if step_counter % 2 == 0:
            current_player = ai_player_X
        else:
            current_player = ai_player_O

        grille.drop(current_player.get_player_symbol(), current_player.play_with_bias(grille))
        player_who_last_played = current_player.get_player_symbol()

        step_counter += 1

    if grille.check_victory():
        winner_symbol = player_who_last_played
    else:
        winner_symbol = 'draw'

    num_steps = grille.get_num_steps()

    if verbose:
        print_victory_screen(grille, winner_symbol)

    return winner_symbol, num_steps


def sp(ai_player):
    """Une partie opposant un joueur humain à une intelligence artificielle"""
    grille = Grille()
    player_who_last_played = None

    human_player = 'X'
    ai_player.player = 'O'

    user_input = []

    step_counter = 0
    while user_input not in ['q'] and not (grille.check_victory()) and len(grille.look_for_allowed_steps()) > 0:

        if step_counter % 2 == 0:
            current_player = human_player

            grille.show_grid()

            while True:
                user_input = input("Letter a through g  = drop disc, q = quit. \nYour move:")
                if user_input in get_possible_player_inputs(grille.width):
                    mon_coup = convert_player_input(user_input)
                    if grille.drop(current_player, mon_coup):
                        break

            player_who_last_played = human_player

        else:
            current_player = ai_player

            grille.drop(current_player.get_player_symbol(), current_player.play_with_bias(grille))

            player_who_last_played = current_player.get_player_symbol()

        step_counter += 1

    if grille.check_victory():
        winner_symbol = player_who_last_played
    else:
        winner_symbol = 'draw'

    num_steps = grille.get_num_steps()

    print_victory_screen(grille, winner_symbol)

    return winner_symbol, num_steps


def pvp():
    """Une partie entre joueurs humains"""
    grid = Grille()

    user_input = []
    player = 'X'
    last_player = None

    while user_input not in ['q'] and not (grid.check_victory()):
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
            print("This ends with a draw. ".format(winner_symbol))

    return


def analyze_AI_self_plays(ai_player_X, ai_player_O, num_parties_jouees):
    num_victoires = {'O': 0, 'X': 0, 'draw': 0}

    for game_no in range(num_parties_jouees):
        winner_symbol, num_steps = np(ai_player_X, ai_player_O, verbose=False)
        print('Game n°{}\tnum_steps={}'.format(game_no + 1, num_steps))
        num_victoires[winner_symbol] += 1

    try:
        ratio_victoires = num_victoires['X'] / (num_victoires['X'] + num_victoires['O'])
    except ZeroDivisionError:
        ratio_victoires = 0.5

    return ratio_victoires


if __name__ == "__main__":
    # Set to None if you want to decide at run-time which kind of play you prefer (AI self-play, human vs. AI, etc.)
    # Set to '0' to let AI vs. AI self-play (useful for Travis integration on Github)
    # Set to '1' to play one game against UCT AI.
    # Set to '2' to allow with no AI, i.e. human vs. human.
    # Set to '3' to compute AI self-play 50 games: UCT AI vs. biased Monte-Carlo AI.

    menu(default_user_action='3', num_parties_jouees=5)
