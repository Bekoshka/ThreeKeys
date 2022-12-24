import pygame
import os

from settings import tile_width, tile_height


def load_image(name, color_key=None, resize=False):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    if resize:
        image = pygame.transform.scale(image, (tile_width, tile_height))
    return image