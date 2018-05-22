def get_conversion_offset():
    return 97


def get_possible_player_inputs(width):
    return [chr(i + get_conversion_offset()) for i in range(width)]


def convert_player_input(player_input):
    return ord(player_input) - get_conversion_offset()


def get_default_mc_params():
    params = dict()
    params['num_tirages_MC'] = 3

    return params


def get_default_uct_params():
    params = dict()
    params['num_tirages_MC'] = 3
    params['num_descentes_dans_arbre'] = 7
    params['facteur_uct'] = 0.0

    return params
