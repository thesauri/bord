import pyxel

class Game:
    def __init__(self):
        self.width = 160
        self.height = 120
        self.table_radius = 8
        self.chair_radius = 2
        self.chair_offset = 2
        self.cart_width = 40
        self.cart_height = 20

        pyxel.init(self.width, self.height, title="Room with Tables and Chairs")

        # Wall properties
        self.wall_thickness = 4

        # Player properties
        self.player_size = 8
        self.player_x = self.width/2 - self.cart_width/4 - self.player_size/2
        self.player_y = self.height - self.cart_height/2 - self.player_size/2
        self.player_speed = 2

        # Cart (for returning stuff)
        self.cart = [
            self.width/2 - self.cart_width/2, self.height - self.cart_height,
            self.cart_width, self.cart_height
        ]

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
            self.width - 2 * self.wall_thickness,
            self.height - 2 * self.wall_thickness,
            0
        )  # Inner room

        # Draw cart
        pyxel.rect(self.cart[0], self.cart[1], self.cart[2], self.cart[3], 1)
        pyxel.rect(self.cart[0] + 1, self.cart[1] + 1, self.cart[2] - 2, self.cart[3] - 1, 2)

        # Draw chairs
        for chair in self.chairs:
            pyxel.circ(chair[0], chair[1], self.chair_radius, 4)
            pyxel.circ(chair[0], chair[1], self.chair_radius - 1, 5)

        # Draw tables
        for table in self.tables:
            pyxel.circ(table[0], table[1], self.table_radius, 4)
            pyxel.circ(table[0], table[1], self.table_radius - 1, 9)

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
