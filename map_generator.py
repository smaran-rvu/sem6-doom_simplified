import numpy as np

from collisions import is_too_close_to_wall, is_wall

# Track positions of spawned entities to avoid clustering
_used_spawn_positions = set()
_MIN_SPAWN_DISTANCE = 2.0  # Minimum distance between spawned entities


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


def generate_map():
    """
    Return a predefined 10x10 map with solid borders and ~20% internal walls (non-crowded).
    1 = wall, 0 = open space.
    """
    # Clear used positions when generating a new map
    _used_spawn_positions.clear()

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


def _distance_between_points(x1, z1, x2, z2):
    """Calculate distance between two points"""
    return np.sqrt((x2 - x1) ** 2 + (z2 - z1) ** 2)


def _too_close_to_other_entities(x, z):
    """Check if position is too close to other spawned entities"""
    for pos_x, pos_z in _used_spawn_positions:
        if _distance_between_points(x, z, pos_x, pos_z) < _MIN_SPAWN_DISTANCE:
            return True
    return False


def get_random_spawn_position(game_map):
    """
    Return a random spawn point in an open area, ensuring it's:
    1. Not in a wall
    2. Not too close to walls
    3. Not too close to other spawned entities
    """
    # Map dimensions
    map_height = len(game_map)
    map_width = len(game_map[0])

    # Maximum attempts to find a suitable position
    max_attempts = 50

    for _ in range(max_attempts):
        # Use floating point coordinates for more variation
        x = np.random.uniform(1.2, map_width - 1.2)
        z = np.random.uniform(1.2, map_height - 1.2)

        # Check if position is valid
        if (
            not is_wall(int(x), int(z), game_map)
            and not is_too_close_to_wall(x, z, game_map)
            and not _too_close_to_other_entities(x, z)
        ):
            # Add to used positions
            _used_spawn_positions.add((x, z))
            return x, z

    # If we couldn't find a good spot after max attempts, try anywhere valid
    for _ in range(max_attempts):
        x = np.random.uniform(1.2, map_width - 1.2)
        z = np.random.uniform(1.2, map_height - 1.2)

        if not is_wall(int(x), int(z), game_map) and not is_too_close_to_wall(
            x, z, game_map
        ):
            _used_spawn_positions.add((x, z))
            return x, z

    # Last resort - find any valid position
    for x in np.linspace(1.5, map_width - 1.5, 10):
        for z in np.linspace(1.5, map_height - 1.5, 10):
            if not is_wall(int(x), int(z), game_map) and not is_too_close_to_wall(
                x, z, game_map
            ):
                _used_spawn_positions.add((x, z))
                return x, z

    # If everything fails, return a known safe spot
    return 5.0, 5.0
