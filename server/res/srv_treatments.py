def treat_answer(request, actual_state):
    answer = eval(request)
    # do the treatment here
    old_position = actual_state["position"]
    new_position = answer["position"]
    new_position = move(old_position, new_position)
    answer["position"] = new_position
    actual_state.update({"position": new_position})
    return actual_state


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
