# For random AI, which is used to simulate end games for every AI!


def get_default_bias_to_obvious_steps():
    # [Warning] Important advice: you might want to keep this boolean to False! Otherwise, there is a huge burden of
    # computation. It might be worth it as the end-game evaluations will be more accurate.
    #
    # Your AI will play obvious steps, no matter this parameter.
    # Only the end-game simulations rely on this parameter.

    bias_to_obvious_steps = False
    return bias_to_obvious_steps


def get_default_max_num_steps_to_explore():
    max_num_steps_to_explore = 10
    return max_num_steps_to_explore


# For both Monte Carlo AI and UCT AI

# noinspection PyPep8Naming
def get_default_num_tirages_MC():
    # noinspection PyPep8Naming
    num_tirages_MC = 14
    return num_tirages_MC


# Only for UCT AI

def get_default_num_descentes_dans_arbre():
    """
    UCT algorithm relies on Monte-Carlo Tree search. However, it differs from MCT because it works in a layered manner.

        repeat 'num_descentes_dans_arbre' times the following procedure:
            - Tree Down: a node is reached based on UCT search criteria,
            - Monte Carlo: the node board state is evaluated using num_tirages_MC samples,
            - Tree Up: the evaluation is propagated up in the search tree using UCT update rules for evaluations.

    """
    num_descentes_dans_arbre = 14
    return num_descentes_dans_arbre


def get_default_facteur_uct():
    """
    The following UCT parameter could be equal to 0.
    However, to take full advantage of the UCT algorithm, use a positive (>0) value.
    """
    facteur_uct = 0.1
    return facteur_uct


# For main

def get_default_num_parties_jouees():
    """
    The number of AI self-play games to find out which of two AI is the best one.
    """
    num_parties_jouees = 10
    return num_parties_jouees
