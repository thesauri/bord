import random
import math
from player import Player

player_radius = 4

class PeePooBot:
    bot_increment = -1
    target_items = [None, None]

    def __init__(self):
        self.target_chair = None
        self.target_table = None
        self.number = PeePooBot.bot_increment + 1
        self.first = True
        
        PeePooBot.bot_increment += 1

    def get_action(self, position: tuple[int, int], capacity: int, chairs: int, tables: int, cart: tuple[float, float, float, float], friends: list[Player], foes: list[Player]):
        # For debugging
        if self.first:
            self.first = False

        if capacity > 3 or (len(chairs) == 0 and len(tables) == 0):
            return get_direction(
                position, [cart[0] + cart[2] / 2, cart[1] + cart[3] / 2]
            )
        if capacity == 0:
            groups = get_groups(tables, chairs)
            best_group = get_largest_closest_group(position, groups, tables)
            closest_item = get_best_item(best_group, position)
            return get_direction(position, closest_item)


        items = [*tables, *chairs]
        # Do not try to pick up tables if no capacity
        if (capacity > 1):
            items = chairs

        if (len(items) > 0):
            closest_item = get_best_item(items, position)
            return get_direction(position, closest_item)


    def get_fill_color(self):
        return 10 if self.number == 0 else 4

    def get_border_color(self):
        return 4 if self.number == 0 else 10

    def get_name_initial_color(self):
        return 10 if self.number == 0 else 4

    def get_name(self):
        return "Pee" if PeePooBot.bot_increment % 2 == 0 else "Poo"

def get_groups(tables, chairs):
    items = [*tables, *chairs]
    groups = []
    used_items_index = []
    for i, item in enumerate(items):
        if i in used_items_index:
            continue
        group = [item]
        for j, other_item in enumerate(items):
            distance = math.dist(item, other_item)
            if distance > 0 and distance < 40:
                group.append(item)
                used_items_index.append(j)
        groups.append(group)
    return groups

    if len(tables) < 1:
        return []
    groups = []
    for table in tables:
        close_chairs = [chair for chair in chairs if math.dist(chair, table) < 13]
        groups.append([table, *close_chairs])
    return groups
        

def get_largest_closest_group(position, groups, tables):
    closest_groups = sorted(groups, key=sort_group_by_distance_fn(position))
    count_group_size = count_group_size_fn(tables)
    largest_group = sorted(groups, key=count_group_size)
    for group in closest_groups:
        if count_group_size(group) >= count_group_size(largest_group):
            return group
    return largest_group[0]


def sort_group_by_distance_fn(pos):
    return lambda group: min([math.dist(item, pos) for item in group])

def count_group_size_fn(tables):
    return lambda group: sum([3 if is_table(tables, item) else 1 for item in group])

def closer_to_pos_fn(pos):
    return lambda item: math.dist(item, pos)

def get_rays():
    return

def is_table(tables, item):
    return item in tables

def get_best_item(items, position):
    closest_items = sorted(items, key=closer_to_pos_fn(position))
    return closest_items[0]

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
