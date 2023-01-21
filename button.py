import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, image, method, x=0, y=0):
        super().__init__()
        self.__method = method
        self.image = image
        self.rect = self.image.get_rect().move(x, y)

    def handle_click(self):
        self.__method()
