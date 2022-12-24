import sys

import pygame

from common import all_sprites
from landscape import Landscape
from player import Player
from settings import WIDTH, HEIGHT, FPS, STEP
from utils import load_image


class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.intro_text = ["ЗАСТАВКА", "",
                      "Правила игры",
                      "Если в правилах несколько строк,",
                      "приходится выводить их построчно"]

    def run(self):
        fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in self.intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру

    def terminate(self):
        pygame.quit()
        sys.exit()


class Camera:
    def __init__(self, focus, other):
        self.focus = focus
        self.other = other
        self.dx = 0
        self.dy = 0
        self.follow()

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)

    def follow(self):
        self.update(self.focus)
        for sprite in self.other:
            self.apply(sprite)


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.landscape = Landscape()
        self.landscape.generate_level()
        self.player = Player(3, 5)
        self.camera = Camera(self.player, all_sprites)
        self.clock = pygame.time.Clock()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(FPS)

    def render(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        all_sprites.draw(self.screen)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                dx, dy = 0, 0
                if keys[pygame.K_LEFT]:
                    dx -= STEP
                if keys[pygame.K_RIGHT]:
                    dx += STEP
                if keys[pygame.K_UP]:
                    dy -= STEP
                if keys[pygame.K_DOWN]:
                    dy += STEP
                self.player.move(dx, dy)
                self.camera.follow()