import pyxel

class Game:
    def __init__(self):
        self.width = 160
        self.height = 120
        self.table_radius = 8
        self.chair_radius = 2
        self.chair_offset = 2

        pyxel.init(self.width, self.height, title="Room with Tables and Chairs")

        # Wall properties
        self.wall_thickness = 4

        # Player properties
        self.player_size = 8
        self.player_x = 80  # Center horizontally
        self.player_y = 100  # Near bottom
        self.player_speed = 2

        # Table properties [x, y, width, height]
        self.tables = [
            [1/4 * self.width, 1/4 * self.height],    # Top left table
            [3/4 * self.width, 1/4 * self.height],   # Top right table
            [1/2 * self.width, 1/2 * self.height],    # Middle
            [1/4 * self.width , 3/4 * self.height],    # Bottom left table
            [3/4 * self.width, 3/4 * self.height],   # Bottom right table
        ]

        # Chair properties [x, y, width, height]
        self.chairs = []
        # Add chairs around each table
        for table in self.tables:
            tx, ty = table
            # Add four chairs: one on each side
            self.chairs.extend([
                [tx, ty - self.table_radius - self.chair_radius - self.chair_offset], # Top
                [tx + self.table_radius + self.chair_radius + self.chair_offset, ty], # Right
                [tx, ty + self.table_radius + self.chair_radius + self.chair_offset], # Bottom
                [tx - self.table_radius - self.chair_radius - self.chair_offset, ty] # Right
            ])

        pyxel.run(self.update, self.draw)

    def would_hit_wall(self, x, y):
        """Check if position would collide with any wall"""
        return (
                x < self.wall_thickness or
                x + self.player_size > 160 - self.wall_thickness or
                y < self.wall_thickness or
                y + self.player_size > 120 - self.wall_thickness
        )

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        original_x = self.player_x
        original_y = self.player_y

        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= self.player_speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += self.player_speed
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y -= self.player_speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y += self.player_speed

        if self.would_hit_wall(self.player_x, self.player_y):
            self.player_x = original_x
            self.player_y = original_y

    def draw(self):
        # Clear screen
        pyxel.cls(1)

        # Draw walls
        pyxel.rect(0, 0, 160, 120, 5)  # Outer wall
        pyxel.rect(
            self.wall_thickness,
            self.wall_thickness,
            160 - 2 * self.wall_thickness,
            120 - 2 * self.wall_thickness,
            0
        )  # Inner room

        # Draw chairs
        for chair in self.chairs:
            pyxel.circ(chair[0], chair[1], self.chair_radius, 4)
            pyxel.circ(chair[0], chair[1], self.chair_radius - 1, 5)
            # pyxel.rect(chair[0], chair[1], chair[2], chair[3], 4)  # Dark brown
            # pyxel.rect(
            #     chair[0] + 1,
            #     chair[1] + 1,
            #     chair[2] - 2,
            #     chair[3] - 2,
            #     5
            # )  # Medium brown

        # Draw tables
        for table in self.tables:
            pyxel.circ(table[0], table[1], self.table_radius, 4)
            pyxel.circ(table[0], table[1], self.table_radius - 1, 9)
            # pyxel.rect(table[0] - table_width / 2, table[1] - table_height / 2, table[0] + table_width / 2, table[1] + table_height / 2, 4)  # Dark brown
            # pyxel.rect(
            #     table[0] - table_width / 2 - 2,
            #     table[1] - table_height / 2 + 2,
            #     table[0] - table_width / 2 + 2,
            #     table[1] - table_height / 2 + 2,
            #     9
            # )  # Light brown

        # Draw player
        pyxel.rect(self.player_x, self.player_y, self.player_size, self.player_size, 8)
        pyxel.rect(
            self.player_x + 1,
            self.player_y + 1,
            self.player_size - 2,
            self.player_size - 2,
            9
        )

Game()
