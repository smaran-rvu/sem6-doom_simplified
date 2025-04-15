# collisions.py
import math


def distance_to_rect(px, pz, rect_x, rect_z):
    """
    Calculate the shortest distance from a point (px, pz) to a rectangle
    defined by the cell with top-left corner (rect_x, rect_z) and size 1x1.
    """
    dx = max(rect_x - px, 0, px - (rect_x + 1))
    dz = max(rect_z - pz, 0, pz - (rect_z + 1))
    return math.sqrt(dx * dx + dz * dz)


def is_too_close_to_wall(x, z, game_map, margin=0.15):
    """
    Check if point (x,z) is within 'margin' distance of any wall cell.
    Only cells near the current grid cell are examined.
    """
    grid_x = int(x)
    grid_z = int(z)
    for i in range(grid_x - 1, grid_x + 2):
        for j in range(grid_z - 1, grid_z + 2):
            if 0 <= i < len(game_map[0]) and 0 <= j < len(game_map):
                if game_map[j][i] == 1:
                    if distance_to_rect(x, z, i, j) < margin:
                        return True
    return False


def is_wall(x, z, game_map):
    """
    Check if the given point (x, z) lies in a wall cell of the game_map.
    """
    map_x = int(x)
    map_z = int(z)
    if 0 <= map_x < len(game_map[0]) and 0 <= map_z < len(game_map):
        return game_map[map_z][map_x] == 1
    return True  # Return true if outside map boundaries
