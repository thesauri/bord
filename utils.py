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


def is_player_hitting_wall(player, width, height, wall_thickness):
    return (
        (player.position[1] < wall_thickness + player.player_radius)
        or (player.position[0] > width - wall_thickness - player.player_radius)
        or (player.position[1] > height - wall_thickness - player.player_radius)
        or (player.position[0] < wall_thickness + player.player_radius)
    )
