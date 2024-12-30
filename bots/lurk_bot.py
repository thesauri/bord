import math

player_radius = 4


class LurkBot:
    secured_role = None

    def __init__(self):
        self.target = 0 if LurkBot.secured_role is None else 1
        LurkBot.secured_role = True

    def get_action(self, position, capacity, chairs, tables, cart, friends, foes):
        if capacity > 1 or (len(chairs) == 0 and len(tables) == 0):
            return get_direction(
                position, [cart[0] + cart[2] / 2, cart[1] + cart[3] / 2]
            )

        dx = 10 if position[0] > 80 else -10
        return get_direction(
            position,
            [
                foes[self.target].position[0] + dx,
                foes[self.target].position[1] - 10,
            ],
        )

    def get_fill_color(self):
        return 0

    def get_border_color(self):
        return 1

    def get_name_initial_color(self):
        return 7

    def get_name(self):
        """Get the name of the bot (maximum 4 characters)"""
        return "LURK" if self.target == 0 else "DERP"


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
