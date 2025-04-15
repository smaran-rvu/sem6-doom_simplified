# main.py

import math

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *

import rendering

# from bullet import Bullet
from collisions import is_too_close_to_wall, is_wall
from constants import (
    ENEMY_DAMAGE,
    ENEMY_HEALTH,
    ENEMY_HEIGHT,
    ENEMY_RESPAWN_TIME,
    FOV,
    MAX_AMMO,
    MAX_ENEMIES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from enemy import Enemy
from map_generator import generate_map, get_random_spawn_position
from player import Player
from texture_loader import load_texture  # Make sure this module is available


def main():
    pygame.init()
    display = (SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.display.gl_set_attribute(pygame.GL_RED_SIZE, 8)
    pygame.display.gl_set_attribute(pygame.GL_GREEN_SIZE, 8)
    pygame.display.gl_set_attribute(pygame.GL_BLUE_SIZE, 8)
    pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)
    pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
    pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)

    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("DOOM-like Game")
    glutInit()  # For GLUT font rendering

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Add lighting configuration
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Set up fixed light in center of map (assuming 10x10 map)
    glLight(
        GL_LIGHT0, GL_POSITION, (5.0, 3.0, 5.0, 1.0)
    )  # Center position (x=5, y=3, z=5)
    glLight(
        GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 0.5)
    )  # Low ambient light for dark corners
    glLight(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))  # Bright diffuse for center

    # Increase attenuation for faster darkness falloff
    glLight(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLight(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.2)  # Increased linear falloff
    glLight(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.08)  # Increased quadratic falloff

    # Simple material properties
    glMaterial(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
    glMaterial(GL_FRONT, GL_SHININESS, 0.0)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(FOV, (display[0] / display[1]), 0.2, 50.0)
    glMatrixMode(GL_MODELVIEW)

    # Load textures (ensure texture paths are correct)
    textures = [
        load_texture("textures/wall.png"),  # 0: Wall texture
        load_texture("textures/enemy.png"),  # 1: Enemy texture
        load_texture("textures/floor.png"),  # 2: Floor texture
        load_texture("textures/ceiling.png"),  # 3: Ceiling texture
        load_texture("textures/bullet.png"),  # 4: Bullet texture
    ]

    player = Player()
    game_map = generate_map()
    enemies = []
    bullets = []

    # Spawn initial enemies
    for _ in range(MAX_ENEMIES):
        enemy = Enemy.spawn_random(game_map, get_random_spawn_position)
        enemies.append(enemy)

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    clock = pygame.time.Clock()

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    player.ammo = MAX_AMMO
                # Find the section where you handle the 'm' key press and update it:
                elif event.key == pygame.K_m:
                    game_map = generate_map()  # This will clear _used_spawn_positions
                    enemies.clear()
                    for _ in range(MAX_ENEMIES):
                        enemies.append(
                            Enemy.spawn_random(game_map, get_random_spawn_position)
                        )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bullet = player.shoot(current_time)
                    if bullet:
                        bullets.append(bullet)
            elif event.type == pygame.MOUSEMOTION:
                player.rotate(-event.rel[0] * 0.1)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(1, game_map, is_wall, is_too_close_to_wall)
        if keys[pygame.K_s]:
            player.move(-1, game_map, is_wall, is_too_close_to_wall)
        if keys[pygame.K_a]:
            player.strafe(1, game_map, is_wall, is_too_close_to_wall)
        if keys[pygame.K_d]:
            player.strafe(-1, game_map, is_wall, is_too_close_to_wall)

        # Update bullets and check collisions with walls/enemies.
        bullets_to_remove = []
        for bullet in bullets:
            bullet.update()
            if is_wall(bullet.position[0], bullet.position[2], game_map):
                bullets_to_remove.append(bullet)
                continue
            for enemy in enemies:
                if not enemy.dead and bullet.check_collision(enemy):
                    bullets_to_remove.append(bullet)
                    enemy.health -= 25
                    if enemy.health <= 0:
                        enemy.dead = True
                        enemy.death_time = current_time
                        player.score += 100
                    break

        for bullet in bullets_to_remove:
            if bullet in bullets:
                bullets.remove(bullet)

        # Update enemy positions and check for collisions/damage.
        for enemy in enemies:
            if not enemy.dead:
                if enemy.move_towards_player(
                    player, game_map, is_wall, is_too_close_to_wall
                ):
                    # Use the take_damage method with cooldown
                    if player.take_damage(ENEMY_DAMAGE, current_time):
                        continue
                        # print(f"Player took damage! Health: {player.health}")

                    if player.health <= 0:
                        print(f"Final Score: {player.score}")
                        print("Game Over")
                        running = False

        # Respawn dead enemies after their respawn time has elapsed.
        for enemy in enemies:
            if enemy.dead and (current_time - enemy.death_time) >= ENEMY_RESPAWN_TIME:
                x, z = get_random_spawn_position(game_map)
                enemy.position = [x, ENEMY_HEIGHT, z]
                enemy.health = ENEMY_HEALTH
                enemy.dead = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # # Update light position to stay centered on player
        # light_pos = [
        #     player.position[0],
        #     player.position[1] + 1.0,  # Light closer to player
        #     player.position[2],
        #     1.0
        # ]
        # glLight(GL_LIGHT0, GL_POSITION, light_pos)

        # Set the camera position and orientation
        gluLookAt(
            player.position[0],
            player.position[1],
            player.position[2],
            player.position[0] - math.sin(math.radians(player.angle)),
            player.position[1],
            player.position[2] - math.cos(math.radians(player.angle)),
            0,
            1,
            0,
        )

        rendering.draw_floor_and_ceiling(textures)
        rendering.draw_walls(game_map, textures)
        rendering.draw_bullets(bullets, textures)
        rendering.draw_enemies(enemies, player, textures)
        rendering.draw_hud(player)
        rendering.draw_crosshair()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
