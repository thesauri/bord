import random

player_radius = 4


class DumbsterBot:
    def __init__(self):
        self.target_chair = None
        self.target_table = None

    def get_action(self, position, capacity, chairs, tables, cart, friends, foes):
        if capacity > 1 or (len(chairs) == 0 and len(tables) == 0):
            return get_direction(
                position, [cart[0] + cart[2] / 2, cart[1] + cart[3] / 2]
            )

        if len(chairs) > 0:
            if self.target_chair is None or self.target_chair not in chairs:
                self.target_chair = random.choice(chairs)
            return get_direction(position, self.target_chair)

        if len(tables) > 0:
            if self.target_table is None or self.target_table not in tables:
                self.target_table = random.choice(tables)
            return get_direction(position, self.target_table)

    def get_fill_color(self):
        return 8

    def get_border_color(self):
        return 7

    def get_name_initial_color(self):
        return 7

    def get_name(self):
        """Get the name of the bot (maximum 4 characters)"""
        return "Dumb"


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
