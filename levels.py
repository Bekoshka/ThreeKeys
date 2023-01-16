import os

from handlers import *
from landscape import *
from creatures import *
from settings import tile_width, tile_height, LEVEL_DIR
from tiles import Obstacle, AnimatedObstacle, Tile


LANDSCAPES = {
    ".": Grass,
    "#": Sand
}


class Level:
    def __init__(self, level, player, game):
        self.game = game
        self.background = self.load_background(level)
        self.objects = self.load_objects(level)
        self.creatures = self.load_creatures(level, player)
        self.handlers = self.load_handlers(level, game)

    def clean(self):
        for i in self.creatures:
            i.clean()
        for i in self.background + self.objects + self.creatures:
            i.kill()
        self.background = []
        self.objects = []
        self.creatures = []
        for i in self.handlers:
            i.clean()
        self.handlers = []

    @staticmethod
    def load_background(level):
        result = []
        with open(os.path.join(LEVEL_DIR, str(level), 'background.txt'), 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        landscape = list(map(lambda x: x.ljust(max_width, '.'), level_map))
        for y in range(len(landscape)):
            for x in range(len(landscape[y])):
                t = landscape[y][x]
                if t in LANDSCAPES.keys():
                    result.append(LANDSCAPES[t](tile_width * x, tile_height * y))
        return result

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
                elif issubclass(cls, Tile):
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
        result.append(ScoreHandler(level, game.game.id))
        result.append(DeathHandler(game))
        return result
