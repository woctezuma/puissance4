def get_conversion_offset():
    return 97


def convert_to_column_display(col):
    return chr(col + get_conversion_offset())


def get_possible_player_inputs(width):
    return [convert_to_column_display(i) for i in range(width)]


def convert_player_input(player_input):
    return ord(player_input) - get_conversion_offset()
