import os

from handlers import *
from landscape import *
from creatures import *
from settings import TILE_WIDTH, TILE_HEIGHT, LEVEL_DIR
from tiles import Obstacle, AnimatedObstacle, Tile


LANDSCAPES = {
    ",": Snow,
    ".": Grass,
    "#": Sand,
    "r": Road,
    "f": Road2,
    "R": Road3,
    "F": Road4,
    "g": Road5,
    "G": Road6,
    "h": Road7,
    "j": SnowRoad1,
    "J": SnowRoad2,
    "k": SnowRoad3,
    "K": SnowRoad4,
    "l": SnowRoad5,
    "L": SnowRoad6,
    "i": Rotate1,
    "I": Rotate2,
    "o": Rotate3,
    "O": Rotate4,
}

OBJECTS = {
    "!": Beton,
    "s": Pine,
    "%": Cactus,
    "c": Rock,
    "w": Forest2,
    "x": SnowPine,
    "q": SnowTree,
    "T": Gates,
    "u": Gates2,
    "p": BrownPortal,
    "P": RedPortal
}

CREATURES = {
    "z": Zombie,
    "Z": Skeleton,
    "d": Scorpion,
    "C": Chest,
    "0": Chest2,
    "1": Chest3,
    "2": Chest4,
    "3": Chest5,
    "4": Chest6,
    "5": Chest7,
    "6": Chest8,
    "B": Boss1,
    "v": ClosedChest,
    "V": ClosedChest2,
    "W": Wolf,
    "b": Cheest1,
    "n": Cheest2,
    "N": Cheest3,
    "m": Cheest4,
    "M": Cheest5,
    "X": Boss2
}


class Level:
    def __init__(self, level, player, game):
        self.__background = self.load_background_grid(level)
        self.__objects = self.load_objects_grid(level) + self.load_objects(level)
        self.__creatures = self.load_creatures_grid(level, player) + self.load_creatures(level, player)
        self.__handlers = self.load_handlers(level, game)

    def clean(self):
        for i in self.__creatures:
            i.clean()
        for i in self.__background + self.__objects + self.__creatures:
            i.kill()
        self.__background = []
        self.__objects = []
        self.__creatures = []
        for i in self.__handlers:
            i.clean()
        self.__handlers = []

    @staticmethod
    def load_background_grid(level):
        grid = Level.load_helper(level, 'background_grid.txt')
        result = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                t = grid[y][x]
                if t in LANDSCAPES.keys():
                    element = LANDSCAPES[t](TILE_WIDTH * x, TILE_HEIGHT * y)
                    result.append(element)
        return result

    @staticmethod
    def load_objects_grid(level):
        grid = Level.load_helper(level, 'objects_grid.txt')
        result = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                t = grid[y][x]
                if t in OBJECTS.keys():
                    element = OBJECTS[t](TILE_WIDTH * x, TILE_HEIGHT * y)
                    result.append(element)
        return result

    @staticmethod
    def load_creatures_grid(level, player):
        grid = Level.load_helper(level, 'creatures_grid.txt')
        result = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                t = grid[y][x]
                if t in CREATURES.keys():
                    if issubclass(CREATURES[t], Player):
                        player.set_position(TILE_WIDTH * x, TILE_HEIGHT * y)
                    elif issubclass(CREATURES[t], Creature):
                        element = CREATURES[t](TILE_WIDTH * x, TILE_HEIGHT * y, player)
                        result.append(element)
        return result

    @staticmethod
    def load_helper(level, file):
        with open(os.path.join(LEVEL_DIR, str(level), file), 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        landscape = list(map(lambda x: x.ljust(max_width, '.'), level_map))
        return landscape

    @staticmethod
    def load_objects(level):
        result = []
        with open(os.path.join(LEVEL_DIR, str(level), 'objects.txt'), 'r') as f:
            for line in f:
                i = line.strip().split()
                cls = globals()[i[0]]
                params = i[1:]
                if issubclass(cls, Obstacle) or issubclass(cls, AnimatedObstacle):
                    result.append(cls(*params))
                else:
                    raise SystemExit("Object can't be loaded: " + i[0])
        return result

    @staticmethod
    def load_creatures(level, player):
        result = []
        with open(os.path.join(LEVEL_DIR, str(level), "creatures.txt"), 'r') as f:
            for line in f:
                i = line.strip().split()
                cls = globals()[i[0]]
                params = i[1:]
                if issubclass(cls, Player):
                    player.set_position(*params)
                elif issubclass(cls, Creature):
                    result.append(cls(*params, player))
                else:
                    raise SystemExit("Creature can't be loaded: " + i[0])
        return result

    @staticmethod
    def load_handlers(level, game):
        result = []
        with open(os.path.join(LEVEL_DIR, str(level), "handlers.txt"), 'r') as f:
            for line in f:
                i = line.strip().split()
                cls = globals()[i[0]]
                params = i[1:]
                if issubclass(cls, TriggerHandler):
                    result.append(cls(*params, game))
                else:
                    raise SystemExit("Handler can't be loaded: " + i[0])
        result.append(ScoreHandler(level, game.get_game_id()))
        result.append(DeathHandler(game))
        return result
