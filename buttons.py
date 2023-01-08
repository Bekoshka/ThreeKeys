import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, image, method, x, y, groups):
        super().__init__(*groups)
        self.method = method
        self.image = image
        self.rect = self.image.get_rect().move(x, y)

    def click(self):
        self.method()