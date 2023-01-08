import os
import sys

import pygame

from common import screen_map_group, monster_group, landscape_group, obstacle_group, player_group, \
    buttons_group, slots_group, items_group, init_common
from events import ScenarioLevel1
from items import Sword, Hood
from creatures import Player, Monster1, Monster2, Monster
from levels import Landscape
from settings import WIDTH, HEIGHT, FPS, SLOT_LEFT_HAND, SLOT_RIGHT_HAND, SLOT_ARMOR, BUTTON_TO_SLOT, DATA_DIR
from tiles import Tile
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
                elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    return

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
        init_common()
        self.cs = ScenarioLevel1()
        self.screen = screen
        self.player = Landscape("1").generate()
        self.camera = Camera(self.player, screen_map_group)
        self.clock = pygame.time.Clock()
        self.running = False

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(FPS)
        return self.cs.is_complete()

    def render(self):
        self.screen.fill(pygame.Color(0, 0, 0))

        landscape_group.draw(self.screen)
        obstacle_group.draw(self.screen)
        monster_group.draw(self.screen)
        player_group.draw(self.screen)

        screen_map_group.update(self.screen)

        slots_group.draw(self.screen)
        items_group.draw(self.screen)
        buttons_group.draw(self.screen)
        items_group.update(self.screen)
        pygame.display.flip()

    def handle_events(self):
        dx, dy = 0, 0
        enemy = None
        button = 0
        keys = pygame.key.get_pressed()
        mods = pygame.key.get_mods()
        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [1, 3]:
                    for monster in monster_group:
                        if monster.rect.collidepoint(event.pos):
                            enemy = monster
                            button = event.button
                    for slot in slots_group:
                        if slot.rect.collidepoint(event.pos):
                            slot.click(mods & pygame.KMOD_SHIFT, mods & pygame.KMOD_CTRL)
                    for btn in buttons_group:
                        if btn.rect.collidepoint(event.pos):
                            btn.click()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_i:
                    self.player.get_inventory().open(True)
                if event.key == pygame.K_a:
                    self.player.get_ammunition().open()
                if event.key == pygame.K_ESCAPE:
                    self.stop()

        if enemy:
            self.player.apply_or_loot(enemy, BUTTON_TO_SLOT[button])
        else:
            self.player.step(dx, dy)
            self.camera.follow()

# TODO LEVELS
# TODO MAKE GAME END TRIGGER ON EVENTS
# TODO SCORE
# TODO SCORE SCREEN

# TODO SHOW ITEM DESCRIPTION ON HOVER

# TODO FIX health bar animation BUG!!

# TODO MAKE SAVE - LOW(PRIO)
# TODO MAKE NEWGAME LOAD BUTTONS - LOW(PRIO)
# TODO RANGE WEAPON - LOW(PRIO)
