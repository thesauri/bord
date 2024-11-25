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
        self.max_capacity = 4
        self.table_capacity = 3
        self.chair_capacity = 1

        pyxel.init(self.width, self.height, title="Room with Tables and Chairs")

        # Wall properties
        self.wall_thickness = 4

        # Player properties
        self.player_radius = 4
        self.player_x = self.width / 2 - self.cart_width / 4 - self.player_radius / 2
        self.player_y = self.height - self.cart_height / 2 - self.player_radius / 2
        self.player_speed = 2
        self.capacity = 0

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

        # Chair properties [x, y, id]
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
                y < self.wall_thickness + self.player_radius or
                x > self.width - self.wall_thickness - self.player_radius or
                y > self.height - self.wall_thickness - self.player_radius or
                x < self.wall_thickness + self.player_radius
        )

    def hits_circular_object(self, position, radius):
        cx, cy = position
        return pow(cx - self.player_x, 2) + pow(cy - self.player_y, 2) < pow(radius + self.player_radius, 2)

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

        for chair in self.chairs:
            if self.hits_circular_object(chair, self.chair_radius) and self.capacity + self.chair_capacity <= self.max_capacity:
                self.capacity += 1
                self.chairs.remove(chair)

        for table in self.tables:
            if self.hits_circular_object(table, self.table_radius) and self.capacity + self.table_capacity <= self.max_capacity:
                self.capacity += 3
                self.tables.remove(table)

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
        pyxel.circ(self.player_x, self.player_y, self.player_radius, 8)
        pyxel.circ(
            self.player_x,
            self.player_y,
            self.player_radius - 1,
            9
        )

        # Draw capacity indicator
        for n in range(0, self.max_capacity):
            red_if_used_otherwise_green = 8 if self.capacity >= n else 11
            pyxel.rect(
                2*n + self.player_x + self.player_radius, self.player_y - self.player_radius - 2,
                1, 1, red_if_used_otherwise_green
            )


Game()
