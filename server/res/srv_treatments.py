def treat_answer(request, identifier):
    answer = eval(request)
    # do the treatment here
    with open(f'{identifier}.json', 'r') as file:
        state = eval(file.read())
        old_position = state["position"]
        new_position = answer["position"]
        new_position = move(old_position, new_position)
        answer["position"] = new_position
        state.update({"position": new_position})
    file.close()
    print(state)
    with open(f'{identifier}.json', 'w') as file:
        file.write(str(state))
    file.close()
    return answer


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
