from random import shuffle

from ai import AI
from ai_interface import InterfaceAI
from grille import Grille
from mc import MC
from uct import UCT


def main():
    trainer_choice = 'MC'  # One of the following texts: 'Random', 'MC', 'UCT'
    num_parties_jouees = 3

    is_consistent = prepare_and_train(trainer_choice, num_parties_jouees)

    assert is_consistent

    return True


def prepare_and_train(trainer_choice='MC', num_parties_jouees=3):
    # Players
    learner = UCT()

    if trainer_choice == 'Random':
        trainer = AI()
    elif trainer_choice == 'MC':
        trainer = MC()
        trainer.equalize_computing_resources(learner)
    else:
        trainer = UCT()

    # Load
    learner.load_model()

    # Train
    learner, num_victories_per_symbol, num_victories_per_player = train(learner, trainer, num_parties_jouees,
                                                                        verbose=True)

    is_consistent = print_stats(num_victories_per_symbol, num_victories_per_player)

    # Save
    learner.save_model()

    return is_consistent


def train(learner, trainer, num_parties_jouees, verbose=False):
    num_victories_per_symbol = {'X': 0, 'O': 0, 'draw': 0}
    num_victories_per_player = {'learner': 0, 'trainer': 0, 'draw': 0}

    # X always starts.
    player_symbols = ['X', 'O']

    # Decide which player is X and which is O.
    learner.player = player_symbols[0]
    trainer.player = player_symbols[1]

    learner.print()
    trainer.print()
    print()

    grille = Grille()

    for game_no in range(num_parties_jouees):

        grille.wipe()

        current_symbol = None
        current_player_name = None

        step_counter = 0
        while not (grille.check_victory()) and len(grille.look_for_allowed_steps()) > 0:

            if step_counter % 2 == 0:
                current_symbol = 'X'
            else:
                current_symbol = 'O'

            if current_symbol == learner.player:
                current_player = learner
                current_player_name = 'learner'
            else:
                current_player = trainer
                current_player_name = 'trainer'

            grille.drop(current_player.get_player_symbol(), current_player.play(grille))
            step_counter += 1

            if verbose:
                grille.show_grid()

        if grille.check_victory():
            winner_symbol = current_symbol
            winner_name = current_player_name
        else:
            winner_symbol = 'draw'
            winner_name = 'draw'

        num_victories_per_symbol[winner_symbol] += 1
        num_victories_per_player[winner_name] += 1

        print(
            'Game n°{}\tnum_steps = {}\twinner = {} ({})'.format(game_no + 1, step_counter, winner_name, winner_symbol))

        # Randomly shuffle symbols assigned to each player
        shuffle(player_symbols)

        # Decide which player is X and which is O.
        learner.player = player_symbols[0]
        trainer.player = player_symbols[1]

    return learner, num_victories_per_symbol, num_victories_per_player


def print_stats(num_victories_per_symbol, num_victories_per_player):
    # Symbols: X vs. O

    num_games_for_symbols = num_victories_per_symbol['X'] \
                            + num_victories_per_symbol['O'] \
                            + num_victories_per_symbol['draw']

    try:
        ratio_victoires_per_symbol = (num_victories_per_symbol['X'] + 0.5 * num_victories_per_symbol['draw']) \
                                     / num_games_for_symbols
    except ZeroDivisionError:
        ratio_victoires_per_symbol = 0.5

    print("\n[Players X vs. O] winrate = {:.2f} (over {} games)".format(ratio_victoires_per_symbol,
                                                                        num_games_for_symbols))

    # Players: Learner vs. Trainer

    num_games_for_players = num_victories_per_player['learner'] \
                            + num_victories_per_player['trainer'] \
                            + num_victories_per_player['draw']

    try:
        ratio_victoires_per_player = (num_victories_per_player['learner'] + 0.5 * num_victories_per_player['draw']) \
                                     / num_games_for_players
    except ZeroDivisionError:
        ratio_victoires_per_player = 0.5

    print("\n[Learner vs. Trainer] winrate = {:.2f} (over {} games)".format(ratio_victoires_per_player,
                                                                            num_games_for_players))

    is_consistent = bool(num_games_for_symbols == num_games_for_players)

    return is_consistent


if __name__ == "__main__":
    main()
