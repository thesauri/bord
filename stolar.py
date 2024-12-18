import pyxel
from dumbster_bot import DumbsterBot
from human_bot import HumanBot


def is_player_overlapping_circular_object(player, position, radius):
    cx, cy = position
    return pow(cx - player.position[0], 2) + pow(cy - player.position[1], 2) < pow(
        radius + player.player_radius, 2
    )


def is_player_overlapping_rectangle(player, rectangle):
    rx, ry, rw, rh = rectangle
    return (
        player.position[0] > rx
        and player.position[1] > ry
        and player.position[0] < rx + rw
        and player.position[1] < ry + rh
    )


def is_player_hitting_player(player1, player2):
    return (
        pow(player1.position[0] - player2.position[0], 2)
        + pow(player1.position[1] - player2.position[1], 2)
    ) < pow(player1.player_radius + player2.player_radius, 2)


class Game:
    def __init__(self):
        self.width = 160
        self.height = 120
        self.table_radius = 8
        self.chair_radius = 2
        self.chair_offset = 2
        self.cart_width = 40
        self.cart_height = 20
        self.table_capacity = 3
        self.chair_capacity = 1
        self.is_game_over = False

        pyxel.init(self.width, self.height, title="Room with Tables and Chairs")

        # Wall properties
        self.wall_thickness = 4

        # Players
        self.players = [
            Player(
                self,
                HumanBot(),
                [
                    self.width / 2 - self.cart_width / 4 - 2,
                    self.height - self.cart_height / 2 - 2,
                ],
            ),
            Player(
                self,
                DumbsterBot(),
                [
                    self.width / 2 + self.cart_width / 4 - 2,
                    self.height - self.cart_height / 2 - 2,
                ],
            ),
        ]

        # Cart (for returning stuff)
        self.cart = [
            self.width / 2 - self.cart_width / 2,
            self.height - self.cart_height,
            self.cart_width,
            self.cart_height,
        ]

        # Table properties [x, y, width, height]
        self.tables = [
            [1 / 4 * self.width, 1 / 4 * self.height],  # Top left table
            [3 / 4 * self.width, 1 / 4 * self.height],  # Top right table
            [1 / 2 * self.width, 1 / 2 * self.height],  # Middle
            [1 / 4 * self.width, 3 / 4 * self.height],  # Bottom left table
            [3 / 4 * self.width, 3 / 4 * self.height],  # Bottom right table
        ]

        # Chair properties [x, y, id]
        self.chairs = []
        # Add chairs around each table
        for table in self.tables:
            tx, ty = table
            # Add four chairs: one on each side
            self.chairs.extend(
                [
                    [
                        tx,
                        ty - self.table_radius - self.chair_radius - self.chair_offset,
                    ],  # Top
                    [
                        tx + self.table_radius + self.chair_radius + self.chair_offset,
                        ty,
                    ],  # Right
                    [
                        tx,
                        ty + self.table_radius + self.chair_radius + self.chair_offset,
                    ],  # Bottom
                    [
                        tx - self.table_radius - self.chair_radius - self.chair_offset,
                        ty,
                    ],  # Right
                ]
            )

        pyxel.run(self.update, self.draw)

    def is_player_hitting_wall(self, player):
        return (
            (player.position[1] < self.wall_thickness + player.player_radius)
            or (
                player.position[0]
                > self.width - self.wall_thickness - player.player_radius
            )
            or (
                player.position[1]
                > self.height - self.wall_thickness - player.player_radius
            )
            or (player.position[0] < self.wall_thickness + player.player_radius)
        )

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        is_all_capacity_zero = True
        for player in self.players:
            if not player.capacity == 0:
                is_all_capacity_zero = False

        if is_all_capacity_zero and len(self.chairs) == 0 and len(self.tables) == 0:
            self.is_game_over = True
            return

        for player in self.players:
            original_position = player.position.copy()

            player.update(self.chairs, self.tables, self.cart)

            if self.is_player_hitting_wall(player):
                player.position = original_position

            for other_player in self.players:
                if player != other_player and is_player_hitting_player(
                    player, other_player
                ):
                    player.position = original_position

            for chair in self.chairs:
                if (
                    is_player_overlapping_circular_object(
                        player, chair, self.chair_radius
                    )
                    and player.capacity + self.chair_capacity <= player.max_capacity
                ):
                    player.capacity += 1
                    self.chairs.remove(chair)

            for table in self.tables:
                if (
                    is_player_overlapping_circular_object(
                        player, table, self.table_radius
                    )
                    and player.capacity + self.table_capacity <= player.max_capacity
                ):
                    player.capacity += 3
                    self.tables.remove(table)

            if is_player_overlapping_rectangle(player, self.cart):
                player.score += player.capacity
                player.capacity = 0

    def draw(self):
        # Clear screen
        pyxel.cls(1)

        # Draw walls
        pyxel.rect(0, 0, self.width, self.height, 5)  # Outer wall
        pyxel.rect(
            self.wall_thickness,
            self.wall_thickness,
            self.width - 2 * self.wall_thickness,
            self.height - 2 * self.wall_thickness,
            0,
        )  # Inner room

        # Draw cart
        pyxel.rect(self.cart[0], self.cart[1], self.cart[2], self.cart[3], 1)
        pyxel.rect(
            self.cart[0] + 1, self.cart[1] + 1, self.cart[2] - 2, self.cart[3] - 1, 2
        )

        # Draw chairs
        for chair in self.chairs:
            pyxel.circ(chair[0], chair[1], self.chair_radius, 4)
            pyxel.circ(chair[0], chair[1], self.chair_radius - 1, 5)

        # Draw tables
        for table in self.tables:
            pyxel.circ(table[0], table[1], self.table_radius, 4)
            pyxel.circ(table[0], table[1], self.table_radius - 1, 9)

        # Draw the players
        for player in self.players:
            pyxel.circ(player.position[0], player.position[1], player.player_radius, 8)
            pyxel.circ(
                player.position[0], player.position[1], player.player_radius - 1, 9
            )

            # Draw capacity indicator
            for n in range(0, player.max_capacity):
                red_if_used_otherwise_green = 8 if player.capacity > n else 11
                pyxel.rect(
                    2 * n + player.position[0] + player.player_radius,
                    player.position[1] - player.player_radius - 2,
                    1,
                    1,
                    red_if_used_otherwise_green,
                )

        if self.is_game_over:
            pyxel.text(
                self.width / 2 - 18,
                self.height / 2 - 20,
                "Game over",
                pyxel.frame_count % 16,
            )

            for i, player in enumerate(self.players):
                pyxel.text(
                    self.width / 2 - 32,
                    self.height / 2 + 10 * i,
                    f"Player {i+1}: {player.score} points",
                    pyxel.frame_count % 16,
                )


class Player:
    def __init__(self, game, bot, start_position):
        self.game = game
        self.bot = bot

        # Player properties
        self.player_radius = 4
        self.position = start_position
        self.player_speed = 2
        self.capacity = 0
        self.max_capacity = 4
        self.score = 0

    def update(self, chairs, tables, cart):
        action = self.bot.get_action(self.position, self.capacity, chairs, tables, cart)

        if action == "LEFT":
            self.position[0] -= self.player_speed
        if action == "RIGHT":
            self.position[0] += self.player_speed
        if action == "UP":
            self.position[1] -= self.player_speed
        if action == "DOWN":
            self.position[1] += self.player_speed


Game()
