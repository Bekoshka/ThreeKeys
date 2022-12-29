import itertools

from common import player_group, monster_group
from settings import KEY_COLOR, VECTORS_TO_DIRECTION
from tiles import Creature, Attackable
from utils import load_image


def load_creature_images(name, frames):
    images = {}
    for dx, dy, n in itertools.product([-1, 0, 1], [-1, 0, 1], range(frames)):
        if not dx and not dy:
            continue
        fname = f'{name}\\{name}_{VECTORS_TO_DIRECTION[dx, dy]}_{n}.png'
        image = load_image(fname, KEY_COLOR)
        if (dx, dy) in images.keys():
            images[dx, dy].append(image)
        else:
            images[dx, dy] = [image]
    return images


class Player(Attackable):
    def __init__(self, pos_x, pos_y):
        images = load_creature_images("mara", 2)
        super().__init__(images, 100, load_image("mara.png", KEY_COLOR), pos_x, pos_y, [player_group])





class Monster(Creature):
    def __init__(self, pos_x, pos_y):
        images = load_creature_images("mara", 2)
        super().__init__(images, 100, pos_x, pos_y, [monster_group])






