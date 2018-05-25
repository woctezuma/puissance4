# For random AI, which is used to simulate end games for every AI!

def get_default_bias_to_obvious_steps():
    return True


def get_default_max_num_steps_to_explore():
    return None


# For both Monte Carlo AI and UCT AI

def get_default_num_tirages_MC():
    return 3


# Only for UCT AI

def get_default_num_descentes_dans_arbre():
    return 7


def get_default_facteur_uct():
    return 0.0
