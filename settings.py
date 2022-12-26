FPS = 120
size = WIDTH, HEIGHT = 800, 600
STEP = 10
tile_width = tile_height = 50


KEY_COLOR = (0xff, 0x5c, 0xf9)

VECTORS_TO_DIRECTION = {
    (1, 0): "R",
    (-1, 0): "L",
    (0, -1): "U",
    (0, 1): "D",
    (1, -1): "UR",
    (-1, -1): "UL",
    (1, 1): "DR",
    (-1, 1): "DL"
}