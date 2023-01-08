import itertools
import os

from settings import VECTORS_TO_DIRECTION, DATA_DIR, KEY_COLOR

# def load_creature_images(name, frames):
#     images = {}
#     for dx, dy, n in itertools.product([-1, 0, 1], [-1, 0, 1], range(frames)):
#         fname = f'{name}\\{name}_{VECTORS_TO_DIRECTION[dx, dy]}_{n}.png'
#         image = load_image(fname, KEY_COLOR)
#         if (dx, dy) in images.keys():
#             images[dx, dy].append(image)
#         else:
#             images[dx, dy] = [image]
#     return images
# import os
from utils import load_image





# def make_dirs(path, mod):
#     for act, dx, dy in itertools.product(["move", "attack-sword"], [-1, 0, 1], [-1, 0, 1]):
#         if dx == dy == 0:
#             continue
#         name = f"""{act}_{dx}_{dy}#{mod}"""
#         print(name, VECTORS_TO_DIRECTION[dx, dy])
#         try:
#             os.makedirs(os.path.join("data", path, name))
#         except FileExistsError:
#             pass


# make_dirs("player", 10)
# load_animation("player")