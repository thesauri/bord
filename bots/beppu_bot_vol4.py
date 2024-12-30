import random
from player import Player
from datetime import datetime


player_radius = 4


class BeppuBotV4:
    def __init__(self):
        self.target_chair = None
        self.target_table = None
        self.target = None

    def get_action(self, position: list[int], capacity: int, chairs: list[list[int]], tables: list[list[int]],
                    cart: list[int], friends: list[Player], foes: list[Player]):
        def internal():
            if capacity >= 4 or (len(chairs) == 0 and len(tables) == 0):
                return get_direction(
                    position, self.fastest_way_back_cart_target(position, cart)
                )

            if len(tables) > 0 and capacity + 3 <= 4:
                closest = sorted(tables+chairs, key=lambda pos: self.min_dist(position, pos))
            else:
                closest = sorted(chairs, key=lambda pos: self.min_dist(position, pos))
            x, y = closest[0]
            return get_direction(position, (x, y+player_radius))
            
        start_time = datetime.now()
        result = internal()
        # print('Duration: {}'.format((datetime.now() - start_time).microseconds))
        return result
    
    def min_dist(self, p1, p2):
        return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

    def fastest_way_back_cart_target(self, pos, cart):
        if pos[0] <= cart[0]: # coming from the left
            return [cart[0]+player_radius+1, cart[1] + cart[3] / 2]
        elif pos[0] >= (cart[0]+cart[2]): # coming from right
            return [int(cart[0]+cart[2]-player_radius-1), cart[1] + cart[3] / 2]
        else:
            return [pos[0], cart[1] + cart[3] / 2]
        

    def get_fill_color(self):
        return 1

    def get_border_color(self):
        return 2

    def get_name_initial_color(self):
        return 3

    def get_name(self):
        """Get the name of the bot (maximum 4 characters)"""
        return "Bep4"


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
