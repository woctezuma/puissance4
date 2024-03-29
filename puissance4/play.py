from random import shuffle

from puissance4.agent.uct import UCT
from puissance4.env.grille import Grille
from puissance4.lib.utils import (
    convert_player_input,
    convert_to_column_display,
    get_possible_player_inputs,
)


def main():
    play_now()

    return True


def play_now(load_previously_trained_model=False):
    # AI player

    ai_player = UCT()

    # Load

    if load_previously_trained_model:
        # Load learnt model
        ai_player.load_model()

    # Play

    play_versus_ai(ai_player)

    return


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

    print(f'Human player is {human_player}')
    print()

    grille = Grille()

    current_symbol = None
    current_player_name = None

    step_counter = 0
    while not (grille.check_victory()) and len(grille.look_for_allowed_steps()) > 0:
        current_symbol = 'X' if step_counter % 2 == 0 else 'O'

        if current_symbol == ai_player.player:
            current_player_name = 'artificial intelligence'

            if step_counter > 0:
                grille.show_grid()

            my_play, is_forced_play = ai_player.play(grille)

            grille.drop(current_symbol, my_play)

        else:
            current_player_name = 'human being'

            grille.show_grid()

            while True:
                user_input = input(
                    "Letter a through g  = drop disc, q = quit. \nYour move:",
                )
                if user_input in get_possible_player_inputs(grille.width):
                    my_play = convert_player_input(user_input)
                    if grille.drop(current_symbol, my_play):
                        break

            is_forced_play = None

        step_counter += 1

        if is_forced_play is not None and is_forced_play:
            print(
                'Obvious play by AI in ({}, {}) below.'.format(
                    current_symbol,
                    convert_to_column_display(my_play).upper(),
                ),
            )

    if grille.check_victory():
        print(
            'Winner = {} ({}) after {} steps'.format(
                current_symbol,
                current_player_name,
                step_counter,
            ),
        )
    else:
        print(f'Draw after {step_counter} steps')

    grille.show_grid()

    return


if __name__ == "__main__":
    main()
