from grille import Grille
from mc import MC
from parameters import get_default_num_parties_jouees
from uct import UCT
from utils import get_possible_player_inputs, convert_player_input


def menu(default_user_action=None, num_parties_jouees=None):
    if num_parties_jouees is None:
        num_parties_jouees = get_default_num_parties_jouees()

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
            # noinspection PyPep8Naming
            player_X = UCT('X')

            # noinspection PyPep8Naming
            player_O = MC('O')
            player_O.equalize_computing_resources(player_X)

            np(player_X, player_O)

            player_X.print()
            player_O.print()

        if user_input == '1':
            # NB: player_X is a human player in this case.

            # noinspection PyPep8Naming
            player_O = UCT('O')

            # Load
            try:
                player_O.load_model()
            except AttributeError:
                print('Learner cannot load a model.')

            sp(player_O)

        if user_input == '2':
            # NB: Both player_X and player_O are human players in this case.

            pvp()

        if user_input == '3':
            # noinspection PyPep8Naming
            player_X = UCT('X')

            # noinspection PyPep8Naming
            player_O = MC('O')
            player_O.equalize_computing_resources(player_X)

            ratio_victoires = analyze_ai_self_plays(player_X, player_O, num_parties_jouees)

            print("\n[Players X vs. O] winrate = {:.2f} (over {} games)".format(ratio_victoires, num_parties_jouees))

            player_X.print()
            player_O.print()

        if default_user_action is not None:
            user_input = 'q'

    return True


# noinspection PyPep8Naming
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

        grille.drop(current_player.get_player_symbol(), current_player.play(grille))
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

            grille.drop(current_player.get_player_symbol(), current_player.play(grille))

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
            print("This ends with a draw.")

    return


# noinspection PyPep8Naming
def analyze_ai_self_plays(ai_player_X, ai_player_O, num_parties_jouees):
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
    # Set to None if you want to decide at run-time which kind of play you prefer among the following ones:
    # Set to '0' to compute one game of AI self-play: UCT AI vs. biased Monte-Carlo AI, with equal computing resources.
    # Set to '1' to let a human player compete against UCT AI.
    # Set to '2' to let two human players compete against each other.
    # Set to '3' to compute N games of AI self-play.

    menu(default_user_action='2')
