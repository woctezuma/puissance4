# For random AI, which is used to simulate end games for every AI!

def get_default_bias_to_obvious_steps():
    bias_to_obvious_steps = True
    return bias_to_obvious_steps


def get_default_max_num_steps_to_explore():
    max_num_steps_to_explore = None
    return max_num_steps_to_explore


# For both Monte Carlo AI and UCT AI

def get_default_num_tirages_MC():
    num_tirages_MC = 3
    return num_tirages_MC


# Only for UCT AI

def get_default_num_descentes_dans_arbre():
    num_descentes_dans_arbre = 7
    return num_descentes_dans_arbre


def get_default_facteur_uct():
    facteur_uct = 0.0
    return facteur_uct
