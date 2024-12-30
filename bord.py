from random import shuffle

import pyxel
from bots.dumbster_bot import DumbsterBot
from bots.human_bot import HumanBot
from time import time
from enum import Enum
import math
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
        self.is_player_collisions_enabled = False
        self.phase = Phase.PRESENTATION
        self.game_started_at_millis = time() * 1_000
        self.countdown_millis = 3 * 1_000
        self.countdown_started_at_millis = None
        self.is_starting_position_randomized = True

        pyxel.init(self.width, self.height, title="Bord")
        pyxel.screen_mode(2)

        pyxel.sounds[Sounds.STARTING.value].set(
            "g#2g#2g#2g#2 g#2g#2g#2g#2 g#2g#2g#2g#2 c#3c#3c#3c#3 c#3c#3",
            "p",
            "7",
            "NNNF NNNF NNNF NNNN NN",
            29,
        )
        pyxel.sounds[Sounds.CHAIR.value].set("e2", "p", "7", "NN", 15)
        pyxel.sounds[Sounds.TABLE.value].set("g#2", "p", "7", "NN", 15)
        pyxel.sounds[Sounds.RETURN.value].set("e2b2b2b2", "p", "7", "NNNN", 15)

        pyxel.sounds[Sounds.FANFARE_MAIN.value].set(
            "e2g#2b2e3 e3b2g#2e2 g#2b2e3g#3 e3b2g#2e2 e2g#2b2e3 g#3e3b2g#2 e2g#2b2e3 e3e3e3e3",
            "p",
            "7777 7777 7777 7777 7777 7777 7777 7777",
            "NNNN NNNN NNNN NNNN NNNN NNNN NNNN VVVV",
            20,
        )

        # Harmony part
        pyxel.sounds[Sounds.FANFARE_HARMONY.value].set(
            "b2e3g#3b3 b3g#3e3b2 e3g#3b3e4 b3g#3e3b2 b2e3g#3b3 e4b3g#3e3 b2e3g#3b3 b3b3b3b3",
            "p",
            "5555 5555 5555 5555 5555 5555 5555 5555",
            "NNNN NNNN NNNN NNNN NNNN NNNN NNNN VVVV",
            20,
        )

        # Bass line
        pyxel.sounds[Sounds.FANFARE_BASS.value].set(
            "e2e2b2b2 e2b2e2b2 e2e2b2b2 e2b2e2b2 e2e2b2b2 e2b2e2b2 e2e2b2b2 e2e2e2e2",
            "p",
            "6666 6666 6666 6666 6666 6666 6666 6666",
            "NNNN NNNN NNNN NNNN NNNN NNNN NNNN VVVV",
            20,
        )

        # Set up the music track with all three parts
        pyxel.musics[0].set(
            [Sounds.FANFARE_MAIN.value],
            [Sounds.FANFARE_HARMONY.value],
            [Sounds.FANFARE_BASS.value],
        )

        # Opening fanfare
        pyxel.sounds[Sounds.OPENING_MAIN.value].set(
            "e3e3e3b3 e4e4e4b3 g#3b3e4g#4 e4b3g#3e3 b2e3g#3b3 e4b3g#3e3 e3g#3b3e4 e4e4e4e4 e4e4e4e4",
            "p",
            "7777 7777 7777 7777 7777 7777 7777 7777 7777",
            "NNNN NNNN NNNN NNNN NNNN NNNN NNNN VVVV VVVV",
            15,
        )

        pyxel.sounds[Sounds.OPENING_HARMONY.value].set(
            "g#3g#3g#3e4 g#4g#4g#4e4 b3e4g#4b4 g#4e4b3g#3 e3g#3b3e4 g#4e4b3g#3 g#3b3e4g#4 b4b4b4b4 b4b4b4b4",
            "p",
            "5555 5555 5555 5555 5555 5555 5555 5555 5555",
            "NNNN NNNN NNNN NNNN NNNN NNNN NNNN VVVV VVVV",
            15,
        )

        pyxel.sounds[Sounds.OPENING_BASS.value].set(
            "e2b2e2b2 e2b2e2b2 e2g#2b2e3 e2b2e2b2 e2b2e2b2 e2b2g#2e2 e2b2e3b3 e2e2e2e2 e2e2e2e2",
            "p",
            "6666 6666 6666 6666 6666 6666 6666 6666 6666",
            "NNNN NNNN NNNN NNNN NNNN NNNN NNNN VVVV VVVV",
            15,
        )
        pyxel.musics[1].set(
            [Sounds.OPENING_MAIN.value],
            [Sounds.OPENING_HARMONY.value],
            [Sounds.OPENING_BASS.value],
        )

        pyxel.playm(1)

        # Wall properties
        self.wall_thickness = 0

        front_positions = [
            [
                self.width / 2 - self.cart_width / 4,
                self.height - 3 * self.cart_height / 4,
            ],
            [
                self.width / 2 + self.cart_width / 4,
                self.height - 3 * self.cart_height / 4,
            ],
        ]
        back_positions = [
            [
                self.width / 2 - self.cart_width / 4,
                self.height - 1 * self.cart_height / 4,
            ],
            [
                self.width / 2 + self.cart_width / 4,
                self.height - 1 * self.cart_height / 4,
            ],
        ]
        if self.is_starting_position_randomized:
            shuffle(front_positions)
            shuffle(back_positions)

        # Players
        player1 = Player(
            self,
            HumanBot(),
            front_positions[0],
        )
        player2 = Player(
            self,
            HumanBot(),
            back_positions[0],
        )
        player3 = Player(
            self,
            DumbsterBot(),
            front_positions[1],
        )
        player4 = Player(
            self,
            DumbsterBot(),
            back_positions[1],
        )

        self.players = [
            player1,
            player2,
            player3,
            player4,
        ]

        # Team up player 1 with player 2 and player 3 with player 4
        self.teams = [
            [player1, player2],
            [player3, player4],
        ]

        player1.set_friends_and_foes([player2], [player3, player4])
        player2.set_friends_and_foes([player1], [player3, player4])
        player3.set_friends_and_foes([player4], [player1, player2])
        player4.set_friends_and_foes([player3], [player1, player2])

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

        match self.phase:
            case Phase.PRESENTATION:
                time_now_millis = time() * 1_000
                millis_elapsed = time_now_millis - self.game_started_at_millis
                if millis_elapsed > 5_000:
                    self.phase = Phase.COUNTDOWN
                    self.countdown_started_at_millis = time_now_millis
                    pyxel.play(0, Sounds.STARTING.value)
                return
            case Phase.COUNTDOWN:
                millis_remaining = self.countdown_millis - (
                    time() * 1_000 - self.countdown_started_at_millis
                )
                if millis_remaining <= 0:
                    self.phase = Phase.PLAYING
                return
            case Phase.PLAYING:
                self.update_game()
                return
            case Phase.GAME_OVER:
                return
            case _:
                return

    def draw(self):
        # Clear screen
        pyxel.cls(1)

        match self.phase:
            case Phase.PRESENTATION:
                self.draw_presentation()
                return
            case Phase.COUNTDOWN:
                self.draw_gameboard()
                self.draw_countdown()
                return
            case Phase.PLAYING:
                self.draw_gameboard()
                return
            case Phase.GAME_OVER:
                self.draw_gameboard()
                self.draw_game_over()
                return
            case _:
                return

    def update_game(self):
        is_all_capacity_zero = True
        for player in self.players:
            if not player.capacity == 0:
                is_all_capacity_zero = False

        if is_all_capacity_zero and len(self.chairs) == 0 and len(self.tables) == 0:
            self.phase = Phase.GAME_OVER
            pyxel.play(0, Sounds.FANFARE_MAIN.value)
            return

        players_with_index = list(enumerate(self.players))
        shuffle(players_with_index)

        for i, player in players_with_index:
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
                    pyxel.play(i, Sounds.CHAIR.value)
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
                    pyxel.play(i, Sounds.TABLE.value)

            if is_player_overlapping_rectangle(player, self.cart):
                previous_score = player.score
                player.score += player.capacity
                player.capacity = 0
                if previous_score != player.score:
                    pyxel.play(i, Sounds.RETURN.value)

    def draw_countdown(self):
        time_remaining_millis = self.countdown_millis - (
            time() * 1_000 - self.countdown_started_at_millis
        )
        time_remaining_seconds = math.ceil(time_remaining_millis / 1_000)
        dy = 2 * math.cos(
            4 * math.pi * (self.countdown_millis - time_remaining_millis) / 1_000
        )
        pyxel.text(
            self.width / 2 - 24,
            self.height / 2 - 10 + dy,
            f"STARTING IN {time_remaining_seconds}",
            7,
        )

    def draw_gameboard(self):
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

    def draw_presentation(self):
        pyxel.text(self.width / 2 - 10, self.height / 2, "VS", 7)

        draw_player(self.players[0], [20, self.height / 2 - 20])
        draw_player(self.players[1], [32, self.height / 2 - 20])
        pyxel.text(
            44,
            self.height / 2 - 22,
            f"{self.players[0].name}&{self.players[1].name}",
            pyxel.frame_count % 16,
        )

        draw_player(self.players[2], [self.width - 20, self.height / 2 + 20])
        draw_player(self.players[3], [self.width - 32, self.height / 2 + 20])
        pyxel.text(
            self.width - 74,
            self.height / 2 + 18,
            f"{self.players[2].name}&{self.players[3].name}",
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
                pyxel.frame_count % 16 if self.phase == Phase.GAME_OVER else 7,
            )

    def draw_game_over(self):
        pyxel.text(
            self.width / 2 - 18,
            self.height / 2 - 10,
            "GAME OVER",
            pyxel.frame_count % 16,
        )


class Phase(Enum):
    PRESENTATION = 1
    COUNTDOWN = 2
    PLAYING = 3
    GAME_OVER = 4


class Sounds(Enum):
    STARTING = 0
    CHAIR = 1
    TABLE = 2
    RETURN = 3
    FANFARE_MAIN = 4
    FANFARE_HARMONY = 5
    FANFARE_BASS = 6
    OPENING_MAIN = 7
    OPENING_HARMONY = 8
    OPENING_BASS = 9


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
