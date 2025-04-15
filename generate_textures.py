import os

import numpy as np
import pygame

# Create textures directory if it doesn't exist
if not os.path.exists("textures"):
    os.makedirs("textures")


# Function to create and save a texture
def create_texture(filename, draw_function):
    surface = pygame.Surface((128, 128), pygame.SRCALPHA)
    draw_function(surface)
    pygame.image.save(surface, os.path.join("textures", filename))
    print(f"Created {filename}")


# Initialize pygame
pygame.init()


# Wall texture (brick pattern)
def draw_wall(surface):
    brick_color = (139, 69, 19)  # Brown
    mortar_color = (169, 169, 169)  # Gray

    # Fill with mortar color
    surface.fill(mortar_color)

    # Draw bricks
    for y in range(0, 128, 32):
        offset = 32 if y % 64 == 0 else 0
        for x in range(offset, 128, 64):
            pygame.draw.rect(surface, brick_color, (x, y, 60, 28))


# Floor texture (checkered pattern)
def draw_floor(surface):
    color1 = (50, 50, 50)  # Dark gray
    color2 = (100, 100, 100)  # Light gray

    # Draw checkered pattern
    for y in range(0, 128, 16):
        for x in range(0, 128, 16):
            color = color1 if (x // 16 + y // 16) % 2 == 0 else color2
            pygame.draw.rect(surface, color, (x, y, 16, 16))


# Ceiling texture
def draw_ceiling(surface):
    base_color = (70, 70, 90)  # Bluish gray

    # Fill with base color
    surface.fill(base_color)

    # Add some noise
    for y in range(128):
        for x in range(128):
            noise = np.random.randint(-10, 10)
            color = tuple(max(0, min(255, c + noise)) for c in base_color)
            surface.set_at((x, y), color)


# Enemy texture (simple monster)
def draw_enemy(surface):
    # Transparent background
    surface.fill((0, 0, 0, 0))

    # Body (red)
    pygame.draw.rect(surface, (200, 0, 0), (32, 32, 64, 80))

    # Eyes (white with black pupils)
    pygame.draw.circle(surface, (255, 255, 255), (48, 48), 12)
    pygame.draw.circle(surface, (255, 255, 255), (80, 48), 12)
    pygame.draw.circle(surface, (0, 0, 0), (48, 48), 6)
    pygame.draw.circle(surface, (0, 0, 0), (80, 48), 6)

    # Mouth (black)
    pygame.draw.rect(surface, (0, 0, 0), (48, 80, 32, 16))


# Bullet texture
def draw_bullet(surface):
    # Transparent background
    surface.fill((0, 0, 0, 0))

    # Metallic bullet color
    bullet_color = (192, 192, 192)  # Silver
    highlight_color = (255, 255, 255)  # White
    shadow_color = (128, 128, 128)  # Dark gray

    # Main bullet body
    pygame.draw.ellipse(surface, bullet_color, (48, 32, 32, 64))
    # Highlight
    pygame.draw.ellipse(surface, highlight_color, (52, 36, 8, 56))
    # Tip
    pygame.draw.polygon(surface, bullet_color, [(48, 32), (80, 32), (64, 16)])


# Create all textures
create_texture("wall.png", draw_wall)
create_texture("floor.png", draw_floor)
create_texture("ceiling.png", draw_ceiling)
create_texture("enemy.png", draw_enemy)
create_texture("bullet.png", draw_bullet)

pygame.quit()
