def move(old_position, new_position):
    # check if the new position is valid

    if not _occupied_position(new_position):
        position = new_position
    else:
        position = old_position

    # check if new position change z position:
    position[2] += _climb_position(position)

    return position


def _occupied_position(position):
    # check if the position is already occupied
    return False


def _climb_position(position):
    # check if it moves z position up or down
    z_increment = 0
    return z_increment
