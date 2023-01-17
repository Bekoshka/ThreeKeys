import pygame

from camera import camera
from settings import WIDTH, HEIGHT


class CameraGroup(pygame.sprite.AbstractGroup):
    def __init__(self, range=(WIDTH // 2 + 100, HEIGHT // 2 + 100)):
        super().__init__()
        self.range = range

    def draw(self, surface):
        sprites = self.__filter()
        self.spritedict.update(
            zip(sprites, surface.blits((spr.image, camera.translate(spr.rect)) for spr in sprites))
        )
        self.lostsprites = []
        dirty = self.lostsprites
        return dirty

    def update(self, *args, **kwargs):
        for sprite in self.__filter():
            sprite.update(*args, **kwargs)

    def __filter(self):
        sprites = []
        for i in self.sprites():
            if abs(i.rect.x - camera.focus.rect.x) > self.range[0]:
                continue
            if abs(i.rect.y - camera.focus.rect.y) > self.range[1]:
                continue
            sprites.append(i)
        return sprites

    def filtered_copy(self):
        group = pygame.sprite.AbstractGroup()
        group.add(self.__filter())
        return group
