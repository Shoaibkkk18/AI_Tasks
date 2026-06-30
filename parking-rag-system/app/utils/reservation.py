def get_next_missing_field(state):

    for field, value in state.items():

        if value is None:
            return field

    return None
