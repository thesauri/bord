import pyxel


class HumanBot:
    def get_action(self, position, capacity, chairs, tables, cart, friends, foes):
        if pyxel.btn(pyxel.KEY_UP):
            return "UP"
        if pyxel.btn(pyxel.KEY_RIGHT):
            return "RIGHT"
        if pyxel.btn(pyxel.KEY_DOWN):
            return "DOWN"
        if pyxel.btn(pyxel.KEY_LEFT):
            return "LEFT"

        return "STOP"

    def get_fill_color(self):
        return 9

    def get_border_color(self):
        return 8

    def get_name_initial_color(self):
        return 7

    def get_name(self):
        """Get the name of the bot (maximum 4 characters)"""
        return "Man"
