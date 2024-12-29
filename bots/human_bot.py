import pyxel


class HumanBot:
    def get_action(self, position, capacity, chairs, tables, cart, players):
        if pyxel.btn(pyxel.KEY_UP):
            return "UP"
        if pyxel.btn(pyxel.KEY_RIGHT):
            return "RIGHT"
        if pyxel.btn(pyxel.KEY_DOWN):
            return "DOWN"
        if pyxel.btn(pyxel.KEY_LEFT):
            return "LEFT"

        return "STOP"

    def get_name(self):
        """Get the name of the bot (maximum 8 characters)"""
        return "Human"
