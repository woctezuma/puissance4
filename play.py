from random import shuffle

from grille import Grille
from uct import UCT
from utils import get_possible_player_inputs, convert_player_input, convert_to_column_display


def main():
    ai_player = UCT()

    # # Load learnt model
    # try:
    #     ai_player.load_model()
    # except AttributeError:
    #     print('Learner cannot load a model.')

    winner_name = play_versus_ai(ai_player)

    return True


def play_versus_ai(ai_player):
    # X always starts.
    player_symbols = ['X', 'O']

    # Randomly shuffle symbols assigned to each player
    shuffle(player_symbols)

    # Decide which player is X and which is O.
    ai_player.player = player_symbols[0]
    human_player = player_symbols[1]

    ai_player.print()
    print()

    print('Human player is {}'.format(human_player))
    print()

    grille = Grille()

    current_symbol = None
    current_player_name = None

    step_counter = 0
    while not (grille.check_victory()) and len(grille.look_for_allowed_steps()) > 0:

        if step_counter % 2 == 0:
            current_symbol = 'X'
        else:
            current_symbol = 'O'

        if current_symbol == ai_player.player:
            current_player = ai_player
            current_player_name = 'artificial intelligence'

            if step_counter > 0:
                grille.show_grid()

            my_play, is_forced_play = current_player.play(grille)

            grille.drop(current_symbol, my_play)

        else:
            current_player = None
            current_player_name = 'human being'

            grille.show_grid()

            user_input = []

            while True:
                user_input = input("Letter a through g  = drop disc, q = quit. \nYour move:")
                if user_input in get_possible_player_inputs(grille.width):
                    my_play = convert_player_input(user_input)
                    if grille.drop(current_symbol, my_play):
                        break

            is_forced_play = None

        step_counter += 1

        if is_forced_play is not None and is_forced_play:
            print('Obvious play by AI in ({}, {}) below.'.format(current_symbol,
                                                                 convert_to_column_display(my_play).upper()))

    if grille.check_victory():
        winner_symbol = current_symbol
        winner_name = current_player_name
        print('Winner = {} ({}) after {} steps'.format(winner_symbol, winner_name, step_counter))
    else:
        winner_symbol = 'draw'
        winner_name = 'draw'
        print('Draw after {} steps'.format(step_counter))

    grille.show_grid()

    return winner_name


if __name__ == "__main__":
    main()
