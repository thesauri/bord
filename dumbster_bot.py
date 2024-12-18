player_radius = 4


class DumbsterBot:
    def get_action(self, position, capacity, chairs, tables, cart):
        if capacity > 1 or (len(chairs) == 0 and len(tables) == 0):
            return get_direction(
                position, [cart[0] + cart[2] / 2, cart[1] + cart[3] / 2]
            )

        if len(chairs) > 0:
            return get_direction(position, chairs[0])

        if len(tables) > 0:
            return get_direction(position, tables[0])


def get_direction(position, target):
    x, y = position
    tx, ty = target

    if ty - y < player_radius:
        return "UP"

    if tx - x > player_radius:
        return "RIGHT"

    if ty - y > player_radius:
        return "DOWN"

    if x - tx > player_radius:
        return "LEFT"

    return "STOP"
