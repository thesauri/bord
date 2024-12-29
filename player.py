class Player:
    def __init__(self, game, bot, start_position):
        self.game = game
        self.bot = bot

        self.player_radius = 4
        self.position = start_position
        self.player_speed = 2
        self.capacity = 0
        self.max_capacity = 4
        self.score = 0

        self.name = bot.get_name().upper()
        if len(self.name) > 4:
            raise ValueError(
                f"The name of the bot ${self.name} must be less than 4 characters"
            )

    def update(self, chairs, tables, cart, players):
        action = self.bot.get_action(
            self.position, self.capacity, chairs, tables, cart, players
        )

        if action == "LEFT":
            self.position[0] -= self.player_speed
        if action == "RIGHT":
            self.position[0] += self.player_speed
        if action == "UP":
            self.position[1] -= self.player_speed
        if action == "DOWN":
            self.position[1] += self.player_speed
