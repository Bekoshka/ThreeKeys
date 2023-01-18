import pygame

from camera import camera
from settings import WIDTH, HEIGHT


class CameraGroup(pygame.sprite.AbstractGroup):
    def __init__(self, ):
        super().__init__()

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
            if abs(i.rect.x - camera.focus.rect.x) > WIDTH:
                continue
            if abs(i.rect.y - camera.focus.rect.y) > HEIGHT:
                continue
            sprites.append(i)
        return sprites

    def filtered_copy(self):
        group = pygame.sprite.AbstractGroup()
        group.add(self.__filter())
        return group