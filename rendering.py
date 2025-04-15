# rendering.py

import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

from constants import BULLET_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH


def draw_walls(game_map, textures):
    glBindTexture(GL_TEXTURE_2D, textures[0])
    for z in range(len(game_map)):
        for x in range(len(game_map[0])):
            if game_map[z][x] == 1:
                glBegin(GL_QUADS)
                # Front face
                glTexCoord2f(0, 0)
                glVertex3f(x, 0, z)
                glTexCoord2f(1, 0)
                glVertex3f(x + 1, 0, z)
                glTexCoord2f(1, 1)
                glVertex3f(x + 1, 2.0, z)
                glTexCoord2f(0, 1)
                glVertex3f(x, 2.0, z)
                # Back face
                glTexCoord2f(0, 0)
                glVertex3f(x, 0, z + 1)
                glTexCoord2f(1, 0)
                glVertex3f(x + 1, 0, z + 1)
                glTexCoord2f(1, 1)
                glVertex3f(x + 1, 2.0, z + 1)
                glTexCoord2f(0, 1)
                glVertex3f(x, 2.0, z + 1)
                # Left face
                glTexCoord2f(0, 0)
                glVertex3f(x, 0, z)
                glTexCoord2f(1, 0)
                glVertex3f(x, 0, z + 1)
                glTexCoord2f(1, 1)
                glVertex3f(x, 2.0, z + 1)
                glTexCoord2f(0, 1)
                glVertex3f(x, 2.0, z)
                # Right face
                glTexCoord2f(0, 0)
                glVertex3f(x + 1, 0, z)
                glTexCoord2f(1, 0)
                glVertex3f(x + 1, 0, z + 1)
                glTexCoord2f(1, 1)
                glVertex3f(x + 1, 2.0, z + 1)
                glTexCoord2f(0, 1)
                glVertex3f(x + 1, 2.0, z)
                # Top face
                glTexCoord2f(0, 0)
                glVertex3f(x, 2.0, z)
                glTexCoord2f(1, 0)
                glVertex3f(x + 1, 2.0, z)
                glTexCoord2f(1, 1)
                glVertex3f(x + 1, 2.0, z + 1)
                glTexCoord2f(0, 1)
                glVertex3f(x, 2.0, z + 1)
                # Bottom face
                glTexCoord2f(0, 0)
                glVertex3f(x, 0, z)
                glTexCoord2f(1, 0)
                glVertex3f(x + 1, 0, z)
                glTexCoord2f(1, 1)
                glVertex3f(x + 1, 0, z + 1)
                glTexCoord2f(0, 1)
                glVertex3f(x, 0, z + 1)
                glEnd()


def draw_floor_and_ceiling(textures):
    # Floor
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(10, 0)
    glVertex3f(10, 0, 0)
    glTexCoord2f(10, 10)
    glVertex3f(10, 0, 10)
    glTexCoord2f(0, 10)
    glVertex3f(0, 0, 10)
    glEnd()
    # Ceiling
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(0, 2.0, 0)
    glTexCoord2f(10, 0)
    glVertex3f(10, 2.0, 0)
    glTexCoord2f(10, 10)
    glVertex3f(10, 2.0, 10)
    glTexCoord2f(0, 10)
    glVertex3f(0, 2.0, 10)
    glEnd()


def draw_enemies(enemies, player, textures):
    sorted_enemies = sorted(
        enemies, key=lambda e: e.distance_to_player(player), reverse=True
    )
    glBindTexture(GL_TEXTURE_2D, textures[1])
    for enemy in sorted_enemies:
        if enemy.dead:
            continue
        dx = player.position[0] - enemy.position[0]
        dz = player.position[2] - enemy.position[2]
        angle_to_player = math.degrees(math.atan2(dx, dz))
        glPushMatrix()
        glTranslatef(enemy.position[0], enemy.position[1], enemy.position[2])
        glRotatef(angle_to_player, 0, 1, 0)
        size = enemy.size
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-size, 0, 0)
        glTexCoord2f(1, 0)
        glVertex3f(size, 0, 0)
        glTexCoord2f(1, 1)
        glVertex3f(size, size, 0)
        glTexCoord2f(0, 1)
        glVertex3f(-size, size, 0)
        glEnd()
        glPopMatrix()


def draw_bullets(bullets, textures):
    glBindTexture(GL_TEXTURE_2D, textures[4])
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet.position[0], bullet.position[1], bullet.position[2])
        angle = math.degrees(math.atan2(bullet.direction[0], bullet.direction[2]))
        glRotatef(angle, 0, 1, 0)
        size = BULLET_SIZE / 2
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-size, -size, 0)
        glTexCoord2f(1, 0)
        glVertex3f(size, -size, 0)
        glTexCoord2f(1, 1)
        glVertex3f(size, size, 0)
        glTexCoord2f(0, 1)
        glVertex3f(-size, size, 0)
        glEnd()
        glPopMatrix()


def draw_hud(player):
    # Switch to orthographic projection
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Disable effects that should not affect HUD
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)  # Disable lighting for HUD elements
    glEnable(GL_BLEND)

    # Draw health bar background (red)
    health_width = 200
    health_height = 20
    x = 10
    y = SCREEN_HEIGHT - 30
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + health_width, y)
    glVertex2f(x + health_width, y + health_height)
    glVertex2f(x, y + health_height)
    glEnd()

    # Draw health bar overlay (green)
    glColor3f(1.0, 1.0, 1.0)
    health_percentage = max(0, player.health / 1000)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + health_width * health_percentage, y)
    glVertex2f(x + health_width * health_percentage, y + health_height)
    glVertex2f(x, y + health_height)
    glEnd()

    # Draw text
    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, SCREEN_HEIGHT - 60, f"Score: {player.score}")
    draw_text(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60, f"Ammo: {player.ammo}/300")


    # Restore matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    # Switch to orthographic projection
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_TEXTURE_2D)  # Add this line
    glEnable(GL_BLEND)
    # Draw health bar background (red)
    health_width = 200
    health_height = 20
    x = 10
    y = SCREEN_HEIGHT - 30
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + health_width, y)
    glVertex2f(x + health_width, y + health_height)
    glVertex2f(x, y + health_height)
    glEnd()

    # Draw health bar overlay (green)
    glColor3f(0.0, 1.0, 0.0)
    health_percentage = max(0, player.health / 1000)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + health_width * health_percentage, y)
    glVertex2f(x + health_width * health_percentage, y + health_height)
    glVertex2f(x, y + health_height)
    glEnd()

    # Draw text (using GLUT bitmap fonts)
    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, SCREEN_HEIGHT - 60, f"Score: {player.score}")
    draw_text(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60, f"Ammo: {player.ammo}/300")

    # Re-enable previously disabled effects
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)  # Re-enable lighting for 3D scene
    

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)  # Add this line
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_text(x, y, text_string):
    glWindowPos2i(x, y)
    for ch in text_string:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def draw_crosshair():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    center_x = SCREEN_WIDTH / 2
    center_y = SCREEN_HEIGHT / 2
    crosshair_size = 10
    glColor3f(1.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(center_x - crosshair_size, center_y)
    glVertex2f(center_x + crosshair_size, center_y)
    glVertex2f(center_x, center_y - crosshair_size)
    glVertex2f(center_x, center_y + crosshair_size)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(1.0)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
