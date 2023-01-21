import pygame

from camera import camera
from settings import WIDTH, HEIGHT


class CameraGroup(pygame.sprite.AbstractGroup):
    def __init__(self, range=(WIDTH // 2 + 100, HEIGHT // 2 + 100)):
        super().__init__()
        self.__range = range

    def draw(self, surface):
        sprites = self.__filter()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(sprites, surface.blits((spr.image, camera.translate(spr.rect)) for spr in sprites))
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, camera.translate(spr.rect))
        self.lostsprites = []
        dirty = self.lostsprites
        return dirty

    def update(self, *args, **kwargs):
        for sprite in self.__filter():
            sprite.update(*args, **kwargs)

    def __filter(self):
        sprites = []
        x, y = camera.get_focus_pos()
        for i in self.sprites():
            if abs(i.rect.x - x) > self.__range[0] or abs(i.rect.y - y) > self.__range[1]:
                continue
            sprites.append(i)
        return sprites

    def filtered_copy(self):
        group = pygame.sprite.AbstractGroup()
        group.add(self.__filter())
        return group
