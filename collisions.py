# collisions.py


def is_too_close_to_wall(x, z, game_map):
    """
    Check if the given position is too close to a wall.
    This is used to prevent getting too close to walls which would look unnatural.
    """
    # Increase the buffer distance from walls
    buffer = 0.3

    # Check positions in 8 directions (including diagonals) to catch corner cases
    return (
        is_wall(x, z, game_map)
        or is_wall(x + buffer, z, game_map)
        or is_wall(x - buffer, z, game_map)
        or is_wall(x, z + buffer, game_map)
        or is_wall(x, z - buffer, game_map)
        # Add diagonal checks
        or is_wall(x + buffer, z + buffer, game_map)
        or is_wall(x - buffer, z - buffer, game_map)
        or is_wall(x + buffer, z - buffer, game_map)
        or is_wall(x - buffer, z + buffer, game_map)
    )


def is_wall(x, z, game_map):
    """Check if the given position is a wall."""
    # Convert float coordinates to integer grid positions
    grid_x, grid_z = int(x), int(z)
    # Return True for walls (value 1), False for open space (value 0)
    return game_map[grid_z][grid_x] == 1
