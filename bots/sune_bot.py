import math

player_radius = 4


class SuneBot:
    targets = []

    def __init__(self):
        pass

    def get_action(self, position, capacity, chairs, tables, cart, friends, foes):
        if len(tables) > 0 and capacity <= 1:
            sorted_tables = sorted(
                tables, key=lambda chair: manhattan_distance(position, chair)
            )
            return get_direction(position, sorted_tables[0])

        if len(chairs) > 0 and capacity < 4:
            sorted_chairs = sorted(
                chairs, key=lambda chair: manhattan_distance(position, chair)
            )
            return get_direction(position, sorted_chairs[0])

        return get_direction(position, [cart[0] + cart[2] / 2, cart[1] + cart[3] / 2])

    def get_fill_color(self):
        return 10

    def get_border_color(self):
        return 5

    def get_name_initial_color(self):
        return 5

    def get_name(self):
        """Get the name of the bot (maximum 4 characters)"""
        return "Tune"


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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
