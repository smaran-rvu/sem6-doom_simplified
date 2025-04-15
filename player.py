# player.py

import math

from bullet import Bullet
from constants import (
    DAMAGE_COOLDOWN,
    MAX_AMMO,
    MOVE_SPEED,
    PLAYER_HEALTH,
    SHOOTING_COOLDOWN,
    TURN_SPEED,
)


class Player:
    def __init__(self):
        self.position = [5.0, 0.5, 5.0]  # x, y, z
        self.angle = 0
        self.health = PLAYER_HEALTH
        self.last_shot_time = 0
        self.last_damage_time = 0
        self.ammo = MAX_AMMO
        self.score = 0

    def move(self, direction, game_map, is_wall, is_too_close_to_wall):
        rad_angle = math.radians(self.angle)
        dx = math.sin(rad_angle) * MOVE_SPEED * direction
        dz = math.cos(rad_angle) * MOVE_SPEED * direction

        new_x = self.position[0] - dx
        new_z = self.position[2] - dz

        # Prevent movement if target position is a wall or too close to one.
        if not is_wall(new_x, new_z, game_map) and not is_too_close_to_wall(
            new_x, new_z, game_map
        ):
            self.position[0] = new_x
            self.position[2] = new_z

    def strafe(self, direction, game_map, is_wall, is_too_close_to_wall):
        rad_angle = math.radians(self.angle + 90)
        dx = math.sin(rad_angle) * MOVE_SPEED * direction
        dz = math.cos(rad_angle) * MOVE_SPEED * direction

        new_x = self.position[0] - dx
        new_z = self.position[2] - dz

        if not is_wall(new_x, new_z, game_map) and not is_too_close_to_wall(
            new_x, new_z, game_map
        ):
            self.position[0] = new_x
            self.position[2] = new_z

    def rotate(self, angle_change):
        self.angle += angle_change * TURN_SPEED
        self.angle %= 360

    def shoot(self, current_time):
        if current_time - self.last_shot_time >= SHOOTING_COOLDOWN and self.ammo > 0:
            self.last_shot_time = current_time
            self.ammo -= 1
            rad_angle = math.radians(self.angle)
            direction = [-math.sin(rad_angle), 0, -math.cos(rad_angle)]
            return Bullet(list(self.position), direction)
        return None

    def take_damage(self, amount, current_time):
        if current_time - self.last_damage_time >= DAMAGE_COOLDOWN:
            self.health -= amount
            self.last_damage_time = current_time
            return True
        return False
