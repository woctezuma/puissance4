def get_conversion_offset():
    return 97


def get_possible_player_inputs(width):
    return [chr(i + get_conversion_offset()) for i in range(width)]


def convert_player_input(player_input):
    return ord(player_input) - get_conversion_offset()
