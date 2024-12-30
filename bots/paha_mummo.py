import random
from player import Player
from dataclasses import dataclass
from copy import copy

player_radius = 4

offs = 4


@dataclass
class Cart:
    x: float
    y: float
    w: float
    h: float

    @property
    def left_corner(self):
        return [self.x + offs, self.y + offs]

    @property
    def right_corner(self):
        return [self.x + self.w - offs, self.y + offs]


def get_dist(
    position: list[float], location: list[float], target_radius: float = None
) -> float:
    return abs(position[0] - location[0]) + abs(position[1] - location[1])


class PahaMummo:
    def __init__(self):
        self.target_chair = None
        self.target = None
        self.prev_collected = 0
        self.prev_position = None
        self.step_size = 0.0

    def get_action(
        self,
        position: list[float, float],
        collected: float,
        chairs: list[list[float, float]],
        tables: list[list[float, float]],
        cart: list[float, float, float, float],
        friends: list[Player],
        foes: list[Player],
    ) -> str:
        cart = Cart(*cart)
        if self.prev_position != position:
            if self.prev_position:
                self.step_size = max(
                    self.step_size, get_dist(self.prev_position, position)
                )
            self.prev_position = position.copy()

        # Detect new collections.
        if collected != self.prev_collected:
            self.prev_collected = collected

        # Go home
        if collected == 4 or (len(chairs) == 0 and len(tables) == 0):
            pos = [cart.left_corner, cart.right_corner]
            dists = [get_dist(position, pos) for pos in pos]
            return get_direction(
                position, pos[dists.index(min(dists))], player_rad=self.step_size
            )

        objects = chairs + tables
        # for friend in friends:
        #     if friend.bot.target:
        #         objects.remove(friend.bot.target)
        objects.sort(key=lambda table: get_dist(position, table))
        self.target = objects[0] if objects else None

        return get_direction(position, self.target)

    def get_fill_color(self):
        return 2

    def get_border_color(self):
        return 7

    def get_name_initial_color(self):
        return 7

    def get_name(self):
        """Get the name of the bot (maximum 4 characters)"""
        return "PAHA"


def get_direction(position, target, player_rad: float = None):
    x, y = position
    tx, ty = target
    if player_rad is None:
        player_rad = player_radius

    if ty - y < player_rad:
        return "UP"

    if tx - x > player_rad:
        return "RIGHT"

    if ty - y > player_rad:
        return "DOWN"

    if x - tx > player_rad:
        return "LEFT"

    return "STOP"
