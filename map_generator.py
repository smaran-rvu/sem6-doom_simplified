import numpy as np

from collisions import is_too_close_to_wall, is_wall


def generate_map(width, height):
    """
    Return a predefined 10x10 map with solid borders and ~20% internal walls (non-crowded).
    1 = wall, 0 = open space.
    """
    return [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # row 0
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],  # row 1
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],  # row 2
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],  # row 3
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],  # row 4
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 1],  # row 5
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],  # row 6
        [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],  # row 7
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # row 8
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # row 9
    ]


def get_random_spawn_position(game_map):
    """
    Return a known safe spawn point — inside an open area with freedom to move.
    """
    x, z = (
        np.random.randint(1, len(game_map) - 1),
        np.random.randint(1, len(game_map[0]) - 1),
    )
    # Check if the position is valid (not a wall and not too close to a wall)
    if not is_wall(int(x), int(z), game_map) and not is_too_close_to_wall(
        x, z, game_map
    ):
        return x, z
    else:
        # If position is not valid, recursively try again
        return get_random_spawn_position(game_map)
