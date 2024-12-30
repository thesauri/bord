import random
from player import Player
from dataclasses import dataclass
from copy import copy

player_radius = 4

offs = 4

table_radius = 8
chair_radius = 2
bias_str = 6


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

    @property
    def front_middle(self):
        return [self.x + self.w / 2, self.y + offs]


def get_dist(
    position: list[float],
    location: list[float],
    target_radius: float = None,
    x_bias: float = 0,
) -> float:
    return abs(position[0] + x_bias - location[0]) + abs(position[1] - location[1])


class PahaMummo:
    def __init__(self):
        self.target_chair = None
        self.target = None
        self.prev_collected = 0
        self.prev_position = None
        self.step_size = 0.0
        self.identity = None

    def home_dist(self, position, cart):
        pos = [cart.left_corner, cart.front_middle, cart.right_corner]
        dists = [get_dist(position, pos) for pos in pos]
        return min(dists)

    def go_home(self, position, cart):
        pos = [cart.left_corner, cart.front_middle, cart.right_corner]
        dists = [get_dist(position, pos) for pos in pos]
        self.target = None
        return get_direction(
            position, pos[dists.index(min(dists))], player_rad=self.step_size
        )

    def infer_id(self, position, cart: Cart):
        # Calculate dists to left and right corner.
        left_dist = get_dist(position, cart.left_corner)
        right_dist = get_dist(position, cart.right_corner)
        if left_dist < right_dist:
            self.x_bias = -bias_str
        else:
            self.x_bias = +bias_str
        return self.x_bias

    def get_action(
        self,
        position: list[float, float],
        collected: float,
        chairs: list[list[float, float]],
        tables: list[list[float, float]],
        cart,
        friends: list[Player],
        foes: list[Player],
    ) -> str:
        cart = Cart(*cart)

        if not self.identity:
            self.identity = self.infer_id(position, cart)

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
            return self.go_home(position, cart)

        if collected <= 1:
            if tables:
                objects = tables.copy()
            else:
                objects = tables.copy() + chairs.copy()
        else:
            objects = chairs.copy()

        foe_predicted_targets = []
        for foe in foes:
            if 0 < foe.capacity < 4:
                their_objects = (
                    chairs.copy() + tables.copy() if collected <= 1 else chairs.copy()
                )
                their_objects.sort(key=lambda ob: get_dist(foe.position, ob))
                their_distance = get_dist(foe.position, their_objects[0])
                foe_predicted_targets.append([their_objects[0], their_distance])

        for friend in friends:
            if friend.bot.target:
                if get_dist(friend.position, friend.bot.target) > get_dist(
                    position, friend.bot.target
                ):
                    continue
                try:
                    objects.remove(friend.bot.target)
                except ValueError:
                    pass
        for foe, their_distance in foe_predicted_targets:
            if their_distance < get_dist(position, foe):
                try:
                    objects.remove(foe)
                except ValueError:
                    pass

        objects.sort(key=lambda ob: get_dist(position, ob, x_bias=self.x_bias))
        self.target = objects[0] if objects else None
        if self.target:
            if collected > 2 and get_dist(position, self.target) > self.home_dist(
                position, cart
            ):
                self.target = None
            if self.target:
                return get_direction(position, self.target)
        return self.go_home(position, cart)

    def get_fill_color(self):
        return 2

    def get_border_color(self):
        return 7

    def get_name_initial_color(self):
        return 7

    def get_name(self):
        """Get the name of the bot (maximum 4 characters)"""
        return random.choice(["PAHA", "MAMA", "OMA", "UBEL", "USEL", "MUMM"])


def get_direction(position, target, player_rad: float = None, target_rad: float = None):
    x, y = position
    tx, ty = target
    if player_rad is None:
        player_rad = player_radius
    if target_rad is None:
        target_rad = 0.0

    if ty - y < player_rad + target_rad:
        return "UP"

    if tx - x > player_rad + target_rad:
        return "RIGHT"

    if ty - y > player_rad + target_rad:
        return "DOWN"

    if x - tx > player_rad + target_rad:
        return "LEFT"

    return "STOP"
