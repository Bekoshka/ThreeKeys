import pygame
import os

from settings import tile_width


def load_image(name, color_key=None, resize=False, size=tile_width):
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
        image = pygame.transform.scale(image, (size, size))
    return image


def calculate_sprite_range(a, b):
    x1, y1, w, h = a.rect
    x1, y1 = x1 + w // 2, y1 + h // 2
    x2, y2, w, h = b.rect
    x2, y2 = x2 + w // 2, y2 + h // 2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5