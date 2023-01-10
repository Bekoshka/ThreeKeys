import pygame
import os

from animation import Animation
from settings import tile_width, DATA_DIR, KEY_COLOR


CACHE = dict()


def cached(func):
    def wrapper(name, color_key=None):
        if (name, str(color_key)) in CACHE.keys():
            return CACHE[name, str(color_key)]
        result = func(name, color_key)
        CACHE[name, str(color_key)] = result
        return result
    return wrapper


@cached
def load_raw_image(name, color_key=None):
    try:
        image = pygame.image.load(name).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_image(name, color_key=None, resize=False, size=tile_width, base=DATA_DIR):
    image = load_raw_image(os.path.join(base, name) if base else name, color_key)

    if resize:
        image = pygame.transform.scale(image, (size, size))
    return image


def load_animations(resource, loop=False):
    animations = {}
    for dir in next(os.walk(os.path.join(DATA_DIR, resource)))[1]:
        name, mod = dir.split('#')
        images = []
        for file in sorted(next(os.walk(os.path.join(DATA_DIR, resource, dir)))[2]):
            images.append(load_raw_image(os.path.join(DATA_DIR, resource, dir, file),
                                         color_key=KEY_COLOR))
        animations[name] = Animation(name, images, int(mod), loop)
    return animations


def calculate_sprite_range(a, b):
    x1, y1, w, h = a.rect
    x1, y1 = x1 + w // 2, y1 + h // 2
    x2, y2, w, h = b.rect
    x2, y2 = x2 + w // 2, y2 + h // 2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5