import math
import random
from player import Player

player_radius = 4

class JumiJamiBot:
    bot_increment = -1
    target_items = [None, None]

    def __init__(self):
        self.target_chair = None
        self.target_table = None
        self.target_item = None
        self.number = JumiJamiBot.bot_increment + 1
        self.first = True
        self.is_top = False
        
        JumiJamiBot.bot_increment += 1

    def get_action(self, position: tuple[int, int], capacity: int, chairs: int, tables: int, cart: tuple[float, float, float, float], friends: list[Player], foes: list[Player]):
        self.target_item = None
        # For debugging

        if self.first:
            self.is_top = is_top(position)
            self.first = False

        if capacity > 3 or (len(chairs) == 0 and len(tables) == 0):
            self.target_item = [cart[0] + cart[2] / 2, cart[1] + cart[3] / 2]
            return get_direction(
                position, [cart[0] + cart[2] / 2, cart[1] + cart[3] / 2], tables
            )
        
        # Early game strategy
        if self.is_top and [80.0, 60.0] in tables:
            return "UP"
        # if self.is_top:
        #     if is_left(position):
        #         if [40.0, 30.0] in tables:
        #             return get_direction(position, [40, 30])
        #     else:
        #         if [120.0, 30.0] in tables:
        #             return get_direction(position, [120.0, 30.0])
        # else:
        #     if is_left(position) and [40.0, 90.0] in tables:
        #         return get_direction(position, [40.0, 90.0])
        #     elif [120.0, 90.0] in tables:
        #         return get_direction(position, [120.0, 90.0])


        if len(tables) > 1 and capacity < 2:
            closest = get_best_item(tables, position, friends[0].bot.target_item, foes, tables)
            return get_direction(position, closest, tables)

        if len(tables) == 1 and capacity < 2:
            closest = get_best_item(tables, position, friends[0].bot.target_item, foes, tables)
            if not (math.dist(friends[0].position, closest) < math.dist(position, closest) and friends[0].capacity < 2):
                return get_direction(position, closest, tables)
            
        
        # if capacity == 0:
        #     groups = get_groups(tables, chairs)
        #     best_group = get_largest_closest_group(position, groups, tables)
        #     closest_item = get_best_item(best_group, position, friends[0].bot.target_item)
        #     self.target_item = closest_item
        #     return get_direction(position, closest_item, tables)


        items = [*tables, *chairs]
        # Do not try to pick up tables if no capacity
        if (capacity > 1):
            items = chairs

        if (len(items) > 0):
            closest_item = get_best_item(items, position, friends[0].bot.target_item, foes, tables)
            self.target_item = closest_item
            return get_direction(position, closest_item, tables)


    def get_fill_color(self):
        return 8 if self.number == 0 else 14

    def get_border_color(self):
        return 8 if self.number == 0 else 2

    def get_name_initial_color(self):
        return 3 if self.number == 0 else 2

    def get_name(self):
        return "Jumi" if JumiJamiBot.bot_increment % 2 == 0 else "Jami"

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

def is_top(pos):
    return pos[1] < 110

def is_left(pos):
    return pos[0] < 80

def is_same_side(pos1, pos2):
    if (is_left(pos1)):
        return is_left(pos2)
    return not is_left(pos2)

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

def get_best_item(items, position, friend_target, foes, tables):
    closest_items = sorted(items, key=closer_to_pos_fn(position))
    for item in closest_items:
        if item == friend_target:
            continue
        item_capa = 3 if is_table(tables, item) else 1
        foes_with_capa = [f for f in foes if f.capacity + item_capa <= 4]
        foes_pos = [f.position for f in foes_with_capa]
        if len(foes_pos) == 0:
            continue
        if min([math.dist(foe_pos, item) for foe_pos in foes_pos]) + 4 < math.dist(position, item) and random.random() > 0.2:
            continue
        return item
    for item in closest_items:
        if item == friend_target:
            continue
        return item
    return closest_items[0]

def get_direction(position, target, tables):
    x, y = position
    tx, ty = target

    offset = 2
    if is_table(tables, target):
        offset = 8
    if math.dist(target, position) < 12:
        offset = 0

    if ty + offset - y < player_radius:
        return "UP"

    if tx - offset - x > player_radius:
        return "RIGHT"

    if ty - offset - y > player_radius:
        return "DOWN"

    if x + offset - tx > player_radius:
        return "LEFT"

    return "RIGHT"
