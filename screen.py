import sys
from itertools import chain

import pygame

from common import screen_map_group, landscape_group, obstacle_group, player_group, \
    buttons_group, slots_group, items_group, corpse_group
from game import Game
from creatures import Player
from levels import Level
from settings import WIDTH, HEIGHT, FPS, GAME_COMPLETED, GAME_FAILED, GAME_PAUSED, GAME_RUNNING
from utils import load_image


class Screen:
    def __init__(self, screen):
        self.screen = screen
        self.running = False
        self.clock = pygame.time.Clock()
        self.delayedRunners = list()

    def _render_background(self, background):
        fon = pygame.transform.scale(background, (WIDTH, HEIGHT))
        self.screen.blit(fon, (0, 0))

    def _render_central_string(self, text):
        font = pygame.font.Font(None, 50)
        string_rendered = font.render(text, True, pygame.Color('black'), pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.center = WIDTH // 2, HEIGHT // 2
        self.screen.blit(string_rendered, intro_rect)

    def _render_text(self, text):
        font = pygame.font.Font(None, 30)
        text_coord = 100
        for line in text:
            string_rendered = font.render(line, True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.__handle_runners()
            self._handle_events()
            self._render()
            self.clock.tick(FPS)

    def __handle_runners(self):
        for runner in self.delayedRunners:
            runner.update()

    def _handle_events(self):
        pass

    def _render(self):
        pass

    def _terminate(self):
        pygame.quit()
        sys.exit()


class StartScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.text = [
            "Открыть инвентарь- I",
            "Надетые вещи- A",
            "Нажмите ЛКМ, чтобы продолжить"
        ]
        self.background = load_image('mount.png')

    def _render(self):
        self._render_background(self.background)
        self._render_text(self.text)
        pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._terminate()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.stop()


class CentralTextScreen(Screen):
    def __init__(self, screen, text):
        self.text = text
        super().__init__(screen)

    def _render(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        self._render_central_string(self.text)
        pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._terminate()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.stop()


class FailScreen(CentralTextScreen):
    def __init__(self, screen):
        super().__init__(screen, "Game Over")


class WinScreen(CentralTextScreen):
    def __init__(self, screen):
        super().__init__(screen, "Congratulations!")


class WinScreen(CentralTextScreen):
    def __init__(self, screen):
        super().__init__(screen, "Congratulations!")


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


class DelayedRunner:
    def __init__(self, wait, callback):
        self.tick_counter = 0
        self.wait = wait
        self.callback = callback

    def update(self):
        self.tick_counter += 1
        if self.tick_counter == self.wait:
            self.callback()


class GameScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.player = Player(3, 5)
        self.levels = [1, 2]
        self.game = Game()
        Game.add(self.game)
        self.current_level = 0

        self.level = Level(self.levels[self.current_level], self.player, self)

        self.camera = Camera(self.player, screen_map_group)
        self.level_complete = False
        self.game_complete = False
        self.player_dead = False

    def get_status(self):
        if self.player_dead:
            return GAME_FAILED
        elif self.game_complete:
            return GAME_COMPLETED
        elif not self.running:
            return GAME_PAUSED
        else:
            return GAME_RUNNING

    def death_delayed(self):
        self.player_dead = True
        self.delayedRunners.append(DelayedRunner(200, self.stop))

    def next_level_delayed(self):
        self.level_complete = True
        self.delayedRunners.append(DelayedRunner(200, self.next_level))

    def clean(self):
        self.level.clean()

    def next_level(self):
        self.level_complete = False
        self.current_level += 1
        self.clean()
        if self.current_level >= len(self.levels):
            self.game_complete = True
            self.stop()
            return
        self.level = Level(self.levels[self.current_level], self.player, self)

    def _render(self):
        self.screen.fill(pygame.Color(0, 0, 0))

        landscape_group.draw(self.screen)
        obstacle_group.draw(self.screen)
        corpse_group.draw(self.screen)
        # monster_group.draw(self.screen)
        player_group.draw(self.screen)

        screen_map_group.update(self.screen)

        slots_group.update(self.screen)
        slots_group.draw(self.screen)
        items_group.draw(self.screen)
        buttons_group.draw(self.screen)
        items_group.update(self.screen)

        self.__render_message()

        pygame.display.flip()

    def __render_message(self):
        if self.player_dead:
            self._render_central_string("YOU ARE DEAD")
        elif self.level_complete:
            self._render_central_string("LEVEL COMPLETE")

    # def render_level_complete(self):
    #     if self.level_complete:
    #         font = pygame.font.Font(None, 50)
    #         for line in ["LEVEL COMPLETE"]:
    #             string_rendered = font.render(line, True, pygame.Color('black'), pygame.Color('white'))
    #             intro_rect = string_rendered.get_rect()
    #             intro_rect.center = WIDTH // 2, HEIGHT // 2
    #             self.screen.blit(string_rendered, intro_rect)

    def _handle_events(self):
        dx, dy = 0, 0
        object = None
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
                    button = event.button
                    for obstacle in chain(obstacle_group, corpse_group):
                        if obstacle.rect.collidepoint(event.pos):
                            object = obstacle
                    for slot in slots_group:
                        if slot.rect.collidepoint(event.pos):
                            slot.handle_click(button, mods & pygame.KMOD_SHIFT, mods & pygame.KMOD_CTRL)
                    for btn in buttons_group:
                        if btn.rect.collidepoint(event.pos):
                            btn.handle_click()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_i:
                    self.player.get_inventory().open(True)
                if event.key == pygame.K_a:
                    self.player.get_ammunition().open()
                if event.key == pygame.K_ESCAPE:
                    self.stop()

        if object:
            self.player.handle_click(object, button)
        else:
            self.player.step(dx, dy)
            self.camera.follow()


# TODO MENU SCREEN
# TODO SCORE SCREEN
# TODO NO LEVEL COMPLETE TIME IN SCORE

# TODO Weapon ATTACK SPEED
# TODO Weapon ATTACH TO VECTOR(ROTATE on mouse)
# TODO HEAL ANIMATION
# TODO MAKE CHEST NOT CREATURE

# TODO REFACTOR TO PRIVATE VARS



# TODO SHOW ITEM DESCRIPTION ON MOUSE3
# TODO FIX health bar animation BUG!!

# TODO MAKE SAVE - LOW(PRIO)
# TODO MAKE NEWGAME LOAD BUTTONS - LOW(PRIO)
# TODO RANGE WEAPON - LOW(PRIO)
