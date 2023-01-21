import pygame


class Window(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect().move(x, y)