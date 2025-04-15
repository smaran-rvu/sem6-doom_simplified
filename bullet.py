# bullet.py

import math

from constants import BULLET_SPEED


class Bullet:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def update(self):
        self.position[0] += self.direction[0] * BULLET_SPEED
        self.position[2] += self.direction[2] * BULLET_SPEED

    def check_collision(self, enemy):
        dx = self.position[0] - enemy.position[0]
        dz = self.position[2] - enemy.position[2]
        distance = math.sqrt(dx * dx + dz * dz)
        return distance < enemy.size
