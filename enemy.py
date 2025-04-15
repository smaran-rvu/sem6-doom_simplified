# enemy.py

import math

from constants import ENEMY_HEALTH, ENEMY_HEIGHT, ENEMY_SPEED


class Enemy:
    def __init__(self, x, z, texture_id):
        self.position = [x, ENEMY_HEIGHT, z]
        self.texture_id = texture_id
        self.size = 0.5
        self.health = ENEMY_HEALTH
        self.dead = False
        self.death_time = 0

    @classmethod
    def spawn_random(cls, game_map, get_random_spawn_position):
        x, z = get_random_spawn_position(game_map)
        return cls(x, z, 1)

    def distance_to_player(self, player):
        dx = self.position[0] - player.position[0]
        dz = self.position[2] - player.position[2]
        return math.sqrt(dx * dx + dz * dz)

    def move_towards_player(self, player, game_map, is_wall, lol):
        if self.dead:
            return

        dx = player.position[0] - self.position[0]
        dz = player.position[2] - self.position[2]
        distance = math.sqrt(dx * dx + dz * dz)

        if distance > 0.5:  # Only move if not too close to the player
            dx /= distance
            dz /= distance

            new_x = self.position[0] + dx * ENEMY_SPEED
            new_z = self.position[2] + dz * ENEMY_SPEED

            if not is_wall(new_x, new_z, game_map):
                self.position[0] = new_x
                self.position[2] = new_z

        if distance < 0.0 + 1e-5:
            distance = 0
        # Return whether the enemy is close enough to inflict damage.
        return distance < 1.5
