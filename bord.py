import pyxel
from bots.dumbster_bot import DumbsterBot
from bots.human_bot import HumanBot
from player import Player
from utils import *


class Game:
    def __init__(self):
        self.width = 160
        self.height = 120
        self.table_radius = 8
        self.chair_radius = 2
        self.chair_offset = 2
        self.cart_width = 40
        self.cart_height = 24
        self.cart_offset = 12
        self.table_capacity = 3
        self.chair_capacity = 1
        self.is_game_over = False
        self.is_player_collisions_enabled = False

        pyxel.init(self.width, self.height, title="Bord")
        pyxel.screen_mode(2)

        # Wall properties
        self.wall_thickness = 0

        # Players
        self.players = [
            Player(
                self,
                HumanBot(),
                [
                    self.width / 2 - self.cart_width / 4,
                    self.height - 3 * self.cart_height / 4,
                ],
            ),
            Player(
                self,
                HumanBot(),
                [
                    self.width / 2 - self.cart_width / 4,
                    self.height - 1 * self.cart_height / 4,
                ],
            ),
            Player(
                self,
                DumbsterBot(),
                [
                    self.width / 2 + self.cart_width / 4,
                    self.height - 3 * self.cart_height / 4,
                ],
            ),
            Player(
                self,
                DumbsterBot(),
                [
                    self.width / 2 + self.cart_width / 4,
                    self.height - 1 * self.cart_height / 4,
                ],
            ),
        ]

        # Team up player 1 with player 2 and player 3 with player 4
        self.teams = [
            [self.players[0], self.players[1]],
            [self.players[2], self.players[3]],
        ]

        self.players[0].set_friends_and_foes(
            [self.players[1]], [self.players[2], self.players[3]]
        )
        self.players[1].set_friends_and_foes(
            [self.players[0]], [self.players[2], self.players[3]]
        )
        self.players[2].set_friends_and_foes(
            [self.players[3]], [self.players[0], self.players[1]]
        )
        self.players[3].set_friends_and_foes(
            [self.players[2]], [self.players[0], self.players[1]]
        )

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

            if is_player_hitting_wall(
                player, self.width, self.height, self.wall_thickness
            ):
                player.position = original_position

            for other_player in self.players:
                if (
                    player != other_player
                    and self.is_player_collisions_enabled
                    and is_player_hitting_player(player, other_player)
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
            draw_player(player, player.position)

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

        self.draw_scoreboard()
        if self.is_game_over:
            pyxel.text(
                self.width / 2 - 18,
                self.height / 2 - 10,
                "GAME OVER",
                pyxel.frame_count % 16,
            )

    def draw_scoreboard(self):
        for i, team in enumerate(self.teams):
            team_score = sum([player.score for player in team])
            player_names = f"{team[0].name}&{team[1].name}"
            alignment_spaces = (9 - len(player_names)) * " "
            draw_player(team[0], [9, 9 + 10 * i])
            draw_player(team[1], [20, 9 + 10 * i])
            pyxel.text(
                29,
                7 + 10 * i,
                f"{player_names}:{alignment_spaces} {team_score}P",
                pyxel.frame_count % 16 if self.is_game_over else 7,
            )


def draw_player(player, position):
    pyxel.circ(
        position[0],
        position[1],
        player.player_radius,
        player.bot.get_border_color(),
    )
    pyxel.circ(
        position[0],
        position[1],
        player.player_radius - 1,
        player.bot.get_fill_color(),
    )
    pyxel.text(
        position[0] - 1,
        position[1] - 2,
        player.name[0],
        player.bot.get_name_initial_color(),
    )


Game()
