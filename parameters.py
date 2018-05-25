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
    num_tirages_MC = 3
    return num_tirages_MC


# Only for UCT AI

def get_default_num_descentes_dans_arbre():
    num_descentes_dans_arbre = 7
    return num_descentes_dans_arbre


def get_default_facteur_uct():
    facteur_uct = 0.0
    return facteur_uct


# For main

def get_default_num_parties_jouees():
    num_parties_jouees = 50
    return num_parties_jouees
