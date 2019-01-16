# For AI interface


def get_default_player_symbol():
    return 'O'


def get_default_check_obvious_plays():
    """
    Parameter regarding obvious plays during games (not during end-game simulations)

    If you AI is not very good, it might help it. Otherwise, it could be better to set this setting to False and try to
    build a better AI with an increase number of Monte Carlo samples. Typically, in UCT vs. MC games, MC benefits from
    this setting, but UCT does not (because UCT's Tree Down algorithm with num_descentes_dans_arbre > num_columns(=7)
    leads to actually checking all the children of the current position, which includes all possible obvious win-steps.

    """
    check_obvious_plays = True
    return check_obvious_plays


# For random AI, which is used to simulate end games for every AI!


def get_default_bias_to_obvious_steps():
    """
    Parameter regarding obvious plays during end-game simulations (not during games)

    [Warning] Important advice: you might want to keep this boolean to False! Otherwise, there is a huge burden of
    computation, which hinders your ability to play with other parameters such as the number of Monte Carlo samples.

    It might sound worth it as the end-game evaluations should be more accurate. However, AI spends most of its
    computation power checking whether each *random* move might be a winning move during end-game simulations, which
    is not a smart way to "think" for an AI. The result is an AI which is less good at the game than it could be.

    AI plays "obvious steps" (one-step win, or one-step win-deny for the opponent), no matter this parameter.
    Only the end-game simulations rely on this parameter.
    """

    bias_to_obvious_steps = True
    return bias_to_obvious_steps


def get_default_max_num_steps_to_explore():
    """
    [Warning] Important advice: you might want to keep this value small. Otherwise, AI will spend a lot of moves to
    evaluate which player wins in each situation, and this will force you to decrease the number of Monte Carlo
    samples. The result is that the value of each board state might be less accurate due to a low num_tirages_MC.

    If max_num_steps_to_explore is set to None, then end-game simulations are simulated until the end (win/loss/draw).
    """

    max_num_steps_to_explore = 30
    return max_num_steps_to_explore


# For both Monte Carlo AI and UCT AI

# noinspection PyPep8Naming
def get_default_num_tirages_MC():
    """
    Number of Monte Carlo samples used to estimate the value of a board state.
    """

    # noinspection PyPep8Naming
    num_tirages_MC = 8
    return num_tirages_MC


def get_default_action_sampling_strategy():
    """
    If true, then we try each allowed first action at the root of the tree, in which case:
     - we spend as much computing resources to value each board state obtained after a first action,
     - the total number of MC samples may slightly differ from 'num_tirages_MC'.

    Otherwise, we randomly sample the first actions at the root of the tree, in which case:
     - we might over-sample or under-sample a few of them,
     - we have a better control of the total number of MC samples.
    """

    deterministic_sampling_of_actions_at_root = True
    return deterministic_sampling_of_actions_at_root


# Only for UCT AI

def get_default_num_descentes_dans_arbre():
    """
    UCT algorithm relies on Monte-Carlo Tree search. However, it differs from MCT because it works in a layered manner.

        repeat 'num_descentes_dans_arbre' times the following procedure:
            - Tree Down: a node is reached based on UCT search criteria,
            - Monte Carlo: the node board state is evaluated using num_tirages_MC samples,
            - Tree Up: the evaluation is propagated up in the search tree using UCT update rules for evaluations.

    """
    num_descentes_dans_arbre = 7
    return num_descentes_dans_arbre


def get_default_facteur_uct():
    """
    The following UCT parameter could be equal to 0. Make sure to use a very small value. Typically, between 0 and 0.3.
    """
    facteur_uct = 0.01
    return facteur_uct


# For main

def get_default_num_parties_jouees():
    """
    The number of AI self-play games to find out which of two AI is the best one.
    """
    num_parties_jouees = 10
    return num_parties_jouees


def main():
    import timeit

    duration = timeit.timeit("prepare_and_train('Random', 10)",
                             setup="from puissance4.training import prepare_and_train",
                             number=1)
    print('Time elapsed = {:.2f} s'.format(duration))

    return


if __name__ == "__main__":
    main()
