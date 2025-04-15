import numpy as np
import pygame
from OpenGL.GL import *


def load_texture(filename):
    """Load a texture from a file and return the OpenGL texture ID."""
    try:
        # Load image using pygame
        surface = pygame.image.load(filename)

        # Convert the image to the right format
        img_data = pygame.image.tostring(surface, "RGBA", True)
        width, height = surface.get_size()

        # Generate a texture ID
        texture_id = glGenTextures(1)

        # Bind the texture
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        # Upload the texture data
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            img_data,
        )

        return texture_id
    except Exception as e:
        print(f"Error loading texture {filename}: {e}")
        # Return a default texture (red)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        # Create a 16x16 red texture
        img_data = np.zeros((16, 16, 4), dtype=np.uint8)
        img_data[:, :, 0] = 255  # Red channel
        img_data[:, :, 3] = 255  # Alpha channel

        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, 16, 16, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data
        )
        return texture_id
