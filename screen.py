import sys
from itertools import chain

import pygame

from animation import animation_tick_counter
from buttons import Button
from common import landscape_group, obstacle_group, buttons_group, slots_group, items_group, \
    corpse_group, mouse, creature_group, animated_obstacle_group, tick_counter
from camera import camera
from delay import DelayedRunner
from game import Game
from creatures import Player
from inventory import Slot
from levels import Level
from score import GameScore
from settings import WIDTH, HEIGHT, FPS, GAME_COMPLETED, GAME_FAILED, GAME_PAUSED, GAME_RUNNING, KEY_COLOR, MENU_NONE, \
    MENU_NEW_GAME, MENU_CONTINUE, MENU_SCORE
from utils import load_image, load_level_list


class Screen:
    def __init__(self, screen):
        self.screen = screen
        self.running = False
        self.clock = pygame.time.Clock()
        self.delayedRunners = list()

    def _render_background(self, background):
        fon = pygame.transform.scale(background, (WIDTH, HEIGHT))
        self.screen.blit(fon, (0, 0))

    def _render_title(self, text):
        font = pygame.font.Font(None, 50)
        string_rendered = font.render(text, True, pygame.Color('WHITE'))
        intro_rect = string_rendered.get_rect()
        intro_rect.center = WIDTH // 2, 50
        self.screen.blit(string_rendered, intro_rect)

    def _render_central_string(self, text):
        font = pygame.font.Font(None, 50)
        string_rendered = font.render(text, True, pygame.Color('black'), pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.center = WIDTH // 2, HEIGHT // 2
        self.screen.blit(string_rendered, intro_rect)

    def _render_text(self, text, font=None, color=pygame.Color('black')):
        if not font:
            font = pygame.font.Font(None, 30)
        text_coord = 100
        for line in text:
            string_rendered = font.render(line, True, color)
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
            runner.check()

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
        self.background = load_image('fon.jpg')

    def _render(self):
        self._render_background(self.background)
        # self._render_text(self.text)
        pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._terminate()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.stop()


class MenuScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.menu_buttons_group = pygame.sprite.Group()
        self.status = MENU_NONE
        self.initialized = False

    def get_status(self):
        return self.status

    def __init(self, game_exist):
        if not self.initialized:
            buttons = [
                ("new_game.png", self.new_game),
                ("continue_game.png", self.continue_game),
                ("score_game.png", self.score_game),
                ("exit_game.png", self._terminate)
            ]
            if not game_exist:
                del buttons[1]
            pos = 100
            border = (HEIGHT - len(buttons) * pos) // 2
            for i, v in enumerate(buttons):
                button = Button(load_image(v[0], KEY_COLOR), v[1])
                button.rect.midtop = (WIDTH // 2, border + pos * i)
                self.menu_buttons_group.add(button)
                self.initialized = True

    def run(self, game_exist):
        self.__init(game_exist)
        super().run()

    def _render(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        self.menu_buttons_group.draw(self.screen)
        pygame.display.flip()

    def __clean(self):
        self.menu_buttons_group.empty()
        self.initialized = False

    def new_game(self):
        self.status = MENU_NEW_GAME
        self.stop()

    def continue_game(self):
        self.status = MENU_CONTINUE
        self.stop()

    def score_game(self):
        self.status = MENU_SCORE
        self.stop()

    def stop(self):
        super().stop()
        self.__clean()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.menu_buttons_group:
                    if btn.rect.collidepoint(event.pos):
                        btn.handle_click()


class ScoreTableScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.game_scores = GameScore.get()

    def _render(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        self._render_title("SCORE")
        lines = [GameScore.title()] + self.game_scores
        self._render_text(map(lambda x: str(x), lines), font=pygame.font.SysFont("monospace", 30),
                          color=pygame.Color("white"))
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


class GameScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.player = Player(3, 5)
        self.levels = load_level_list()
        self.game = Game()
        Game.add(self.game)
        self.current_level = 0

        self.level = Level(self.levels[self.current_level], self.player, self)

        camera.focus = self.player
        self.level_complete = False
        self.game_complete = False
        self.player_dead = False

    def get_player(self):
        return self.player

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

    def exit(self):
        self.clean()
        self.player.kill()
        self.player.clean()
        self.stop()

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
        corpse_group.draw(self.screen)
        obstacle_group.draw(self.screen)

        animated_obstacle_group.update(self.screen)
        creature_group.update(self.screen)

        slots_group.update(self.screen)
        slots_group.draw(self.screen)
        items_group.draw(self.screen)
        buttons_group.draw(self.screen)
        items_group.update(self.screen)

        Slot.render_description(self.screen)

        self.__render_message()

        tick_counter.next()
        animation_tick_counter.next()

        pygame.display.flip()

    def __render_message(self):
        if self.player_dead:
            self._render_central_string("YOU ARE DEAD")
        elif self.level_complete:
            self._render_central_string("LEVEL COMPLETE")

    def _handle_events(self):
        mouse.set_pos(pygame.mouse.get_pos())

        dx, dy = 0, 0
        object = None
        button = 0
        keys = pygame.key.get_pressed()
        mods = pygame.key.get_mods()
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [1, 2, 3]:
                    button = event.button
                    for obstacle in chain(obstacle_group, corpse_group):
                        if camera.translate(obstacle.rect).collidepoint(event.pos):
                            object = obstacle
                    for slot in slots_group:
                        if slot.rect.collidepoint(event.pos):
                            slot.handle_click(button, mods & pygame.KMOD_SHIFT, mods & pygame.KMOD_CTRL)
                    for btn in buttons_group:
                        if btn.rect.collidepoint(event.pos):
                            btn.handle_click()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    Slot.clean_description()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    self.player.get_inventory().open(True)
                if event.key == pygame.K_q:
                    self.player.get_ammunition().open()
                if event.key == pygame.K_ESCAPE:
                    self.stop()

        if object:
            self.player.handle_click(object, button)
        else:
            self.player.step(dx, dy)
            camera.follow()


# TODO step, ai_mod, aggr_range

# TODO REFACTOR TO PRIVATE VARS
