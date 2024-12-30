import math

player_radius = 4


class TureBot:
    def __init__(self):
        self.target = None

    def get_action(self, position, capacity, chairs, tables, cart, friends, foes):
        if self.target != None and (self.target in chairs or self.target in tables):
            get_direction(position, self.target)

        cart_target = closest_point_on_cart(position, cart)
        distance_home = manhattan_distance(position, cart_target)

        best_target = None
        best_target_award = 0

        if capacity <= 1 and len(tables) > 0:
            closest_winnable_target = get_closest_winnable_target(
                position, tables, foes
            )
            if closest_winnable_target is not None:
                best_target = closest_winnable_target
                best_target_award = 3

        if capacity < 4 and len(chairs) > 0:
            closest_winnable_target = get_closest_winnable_target(
                position, chairs, foes
            )
            if best_target is None and closest_winnable_target is not None:
                best_target = closest_winnable_target
                best_target_award = 1

        distance_to_best_target = (
            manhattan_distance(position, best_target)
            if best_target is not None
            else math.inf
        )

        has_haul_and_is_close_to_home = (
            capacity > 0 and 2 * distance_home < distance_to_best_target
        )
        if has_haul_and_is_close_to_home or best_target is None:
            middle_of_cart = [cart[0] + cart[2] / 2, cart[1] + cart[3] / 2]
            return get_direction(position, middle_of_cart)

        self.target = best_target
        return get_direction(position, best_target)

    def get_fill_color(self):
        return 5

    def get_border_color(self):
        return 10

    def get_name_initial_color(self):
        return 10

    def get_name(self):
        """Get the name of the bot (maximum 4 characters)"""
        return "Ture"


class SuneBot:
    def __init__(self):
        self.target = None

    def get_action(self, position, capacity, chairs, tables, cart, friends, foes):
        if self.target != None and (self.target in chairs or self.target in tables):
            get_direction(position, self.target)

        cart_target = closest_point_on_cart(position, cart)
        distance_home = manhattan_distance(position, cart_target)

        best_target = None
        best_target_award = 0

        if capacity < 4 and len(chairs) > 0:
            closest_winnable_target = get_closest_winnable_target(
                position, chairs, foes
            )
            if best_target is None and closest_winnable_target is not None:
                best_target = closest_winnable_target
                best_target_award = 1

        if capacity <= 1 and len(tables) > 0:
            closest_winnable_target = get_closest_winnable_target(
                position, tables, foes
            )
            if closest_winnable_target is not None:
                best_target = closest_winnable_target
                best_target_award = 3

        distance_to_best_target = (
            manhattan_distance(position, best_target)
            if best_target is not None
            else math.inf
        )

        has_haul_and_is_close_to_home = (
            capacity > 0 and 2 * distance_home < distance_to_best_target
        )
        if has_haul_and_is_close_to_home or best_target is None:
            middle_of_cart = [cart[0] + cart[2] / 2, cart[1] + cart[3] / 2]
            return get_direction(position, middle_of_cart)

        self.target = best_target
        return get_direction(position, best_target)

    def get_fill_color(self):
        return 10

    def get_border_color(self):
        return 5

    def get_name_initial_color(self):
        return 5

    def get_name(self):
        """Get the name of the bot (maximum 4 characters)"""
        return "Sune"


def closest_point_on_cart(position, cart):
    px = position[0]
    py = position[1]
    cx1 = cart[0]
    cy1 = cart[1]
    cx2 = cart[0] + cart[2]
    cy2 = cart[1] + cart[3]

    x = cx1 if px < cx1 else cx2
    y = cy1 if py < cy1 else cy2

    return [x, y]


def manhattan_distance(position1, position2):
    x1, y1 = position1
    x2, y2 = position2
    return abs(x1 - x2) + abs(y1 - y2)


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


def get_closest_winnable_target(position, targets, foes):
    closest_winnable_target = None
    closest_winnable_distance = math.inf
    is_guaranteed = False

    for target in targets:
        distance = manhattan_distance(position, target)

        closest_distance_for_foe = math.inf
        for foe in foes:
            if foe.capacity > 1:
                continue
            foe_distance = manhattan_distance(foe.position, target)
            if foe_distance < closest_distance_for_foe:
                closest_distance_for_foe = foe_distance

        if distance < closest_winnable_distance:
            if is_guaranteed and closest_distance_for_foe < distance:
                continue

            is_guaranteed = distance < closest_distance_for_foe
            closest_winnable_target = target
            closest_winnable_distance = distance

    return closest_winnable_target
