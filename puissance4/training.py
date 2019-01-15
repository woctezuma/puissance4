from random import shuffle

from .agent.ai import AI
from .agent.mc import MC
from .agent.uct import UCT
from .env.grille import Grille
from .lib.utils import convert_to_column_display


def main():
    test_range_of_parameters()

    return True


def test_range_of_parameters(load_and_save_model=False):
    trainer_choice = 'UCT'  # One of the following texts: 'Random', 'MC', 'UCT'
    num_parties_jouees = 200

    results = dict()

    for num_tirages_MC in [8]:
        for num_descentes_dans_arbre in range(6, 14, 2):
            for facteur_uct in [0]:
                for max_num_steps_to_explore in [30]:
                    _, num_victories, num_steps = prepare_and_train(trainer_choice, num_parties_jouees,
                                                                    num_tirages_MC=num_tirages_MC,
                                                                    num_descentes_dans_arbre=num_descentes_dans_arbre,
                                                                    facteur_uct=facteur_uct,
                                                                    max_num_steps_to_explore=max_num_steps_to_explore,
                                                                    load_and_save_previously_trained_model=load_and_save_model)

                    num_victories['average_num_steps'] = sum(num_steps) / len(num_steps)
                    results[(num_tirages_MC, num_descentes_dans_arbre, facteur_uct, max_num_steps_to_explore)] \
                        = num_victories

                    print('Temporary summary: {}'.format(repr(results)))
                    print('\nAverage number of steps: {}'.format(num_victories['average_num_steps']))

    print('Final summary: {}'.format(repr(results)))

    return


# noinspection PyPep8Naming
def prepare_and_train(trainer_choice='MC', num_parties_jouees=3,
                      num_tirages_MC=None,
                      num_descentes_dans_arbre=None,
                      facteur_uct=None,
                      max_num_steps_to_explore=None,
                      bias_to_obvious_steps=None,
                      check_obvious_plays=None,
                      deterministic_root_action_sample=True,
                      enforce_identical_computing_resources=True,
                      load_and_save_previously_trained_model=False):
    # AI player which is learning by playing against the "trainer"
    learner = UCT()

    if num_tirages_MC is not None:
        learner.num_tirages_MC = num_tirages_MC

    if num_descentes_dans_arbre is not None:
        learner.num_descentes_dans_arbre = num_descentes_dans_arbre

    if facteur_uct is not None:
        learner.facteur_uct = facteur_uct

    if max_num_steps_to_explore is not None:
        learner.max_num_steps_to_explore = max_num_steps_to_explore

    if bias_to_obvious_steps is not None:
        learner.bias_to_obvious_steps = bias_to_obvious_steps

    if check_obvious_plays is not None:
        learner.check_obvious_plays = check_obvious_plays

    # AI player which is training the "learner"

    if trainer_choice == 'Random':
        trainer = AI()
    elif trainer_choice == 'MC':
        trainer = MC()
        trainer.deterministic_sampling_of_actions_at_root = deterministic_root_action_sample
    else:
        trainer = UCT()

    if enforce_identical_computing_resources:
        trainer.equalize_computing_resources(learner)

    # Load

    if load_and_save_previously_trained_model:
        learner.load_model()

    # Train
    learner, num_victories, num_victories_per_symbol, num_victories_per_player, num_steps = train(learner,
                                                                                                  trainer,
                                                                                                  num_parties_jouees,
                                                                                                  verbose=False)

    # Print

    learner.print()

    is_consistent = print_stats(num_victories, num_victories_per_symbol, num_victories_per_player)

    # Save

    if load_and_save_previously_trained_model:
        learner.save_model()

    return is_consistent, num_victories, num_steps


def train(learner, trainer, num_parties_jouees, verbose=False):
    num_victories_per_symbol = {'X': 0, 'O': 0, 'draw': 0}
    num_victories_per_player = {'learner': 0, 'trainer': 0, 'draw': 0}

    # X always starts.
    player_symbols = ['X', 'O']

    num_victories = {'draw': 0}
    for element in ['learner', 'trainer']:
        for symbol in player_symbols:
            num_victories[(element, symbol)] = 0

    # Decide which player is X and which is O.
    learner.player = player_symbols[0]
    trainer.player = player_symbols[1]

    learner.print()
    trainer.print()
    print()

    num_steps = []

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

            my_play, is_forced_play = current_player.play(grille)

            if verbose:
                if is_forced_play is not None and is_forced_play:
                    print(
                        'Obvious play by {} in ({}, {}) below.'.format(current_player_name, current_symbol,
                                                                       convert_to_column_display(my_play).upper()))

            grille.drop(current_player.get_player_symbol(), my_play)
            step_counter += 1

            if verbose:
                grille.show_grid()

        if grille.check_victory():
            winner_symbol = current_symbol
            winner_name = current_player_name
            num_victories[(winner_name, winner_symbol)] += 1
        else:
            winner_symbol = 'draw'
            winner_name = 'draw'
            num_victories['draw'] += 1

        num_victories_per_symbol[winner_symbol] += 1
        num_victories_per_player[winner_name] += 1

        print(
            'Game n°{}\tnum_steps = {}\twinner = {} ({})'.format(game_no + 1, step_counter, winner_name, winner_symbol))

        num_steps.append(step_counter)

        # Randomly shuffle symbols assigned to each player
        shuffle(player_symbols)

        # Decide which player is X and which is O.
        learner.player = player_symbols[0]
        trainer.player = player_symbols[1]

    return learner, num_victories, num_victories_per_symbol, num_victories_per_player, num_steps


def print_stats(num_victories, num_victories_per_symbol, num_victories_per_player):
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

    # Additional print, useful to check everything works as intended, e.g. that the learnt model works for both X and O.
    print()
    print(num_victories)
    print(num_victories_per_symbol)
    print(num_victories_per_player)

    return is_consistent


if __name__ == "__main__":
    main()
