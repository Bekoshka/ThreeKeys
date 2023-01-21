import sys
from itertools import chain

import pygame

from animation import animation_tick_counter
from button import Button
from camera import camera
from common import landscape_group, obstacle_group, buttons_group, slots_group, items_group, \
    corpse_group, mouse, creature_group, animated_obstacle_group, tick_counter, window_groups
from delay import DelayedRunner
from game import Game
from creature import Player
from inventory import Slot
from level import Level
from gamescore import GameScore
from settings import WIDTH, HEIGHT, FPS
from globals import GAME_COMPLETED, GAME_FAILED, GAME_PAUSED, GAME_RUNNING, KEY_COLOR, MENU_NONE, \
    MENU_NEW_GAME, MENU_CONTINUE, MENU_SCORE, MENU_HOTKEYS
from util import load_image, load_level_list


class Screen:
    def __init__(self, screen):
        self._screen = screen
        self.__running = False
        self.__clock = pygame.time.Clock()
        self.__delayedRunners = list()

    def _append_delayed_runners(self, runner):
        self.__delayedRunners.append(runner)

    def _clean_delayed_runners(self):
        self.__delayedRunners.clear()

    def _render_background(self, background):
        fon = pygame.transform.scale(background, (WIDTH, HEIGHT))
        self._screen.blit(fon, (0, 0))

    def _render_central_string(self, text, color=pygame.Color('BLACK'), bg_color=None, pos=(0, 0)):
        font = pygame.font.Font(None, 50)
        string_rendered = font.render(text, True, color, bg_color)
        intro_rect = string_rendered.get_rect()
        intro_rect.center = pos
        self._screen.blit(string_rendered, intro_rect)

    def _render_text(self, text, font=None, color=pygame.Color('BLACK'), bg_color=None, pos=(0, 0)):
        if not font:
            font = pygame.font.Font(None, 30)
        text_x, text_y = pos
        for line in text:
            string_rendered = font.render(line, True, color, bg_color)
            intro_rect = string_rendered.get_rect()
            intro_rect.topleft = text_x, text_y
            text_y += intro_rect.height
            self._screen.blit(string_rendered, intro_rect)

    def is_running(self):
        return self.__running

    def stop(self):
        self.__running = False

    def run(self):
        self.__running = True
        while self.__running:
            self.__handle_runners()
            self._handle_events()
            self._render()
            self.__clock.tick(FPS)

    def __handle_runners(self):
        for runner in self.__delayedRunners:
            runner.check()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._terminate()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.stop()

    def _render(self):
        pass

    @staticmethod
    def _terminate():
        pygame.quit()
        sys.exit()


class StartScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.background = load_image('fon.jpg')

    def _render(self):
        self._render_background(self.background)
        pygame.display.flip()


class HotkeysScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.text = [
            "КАРТА:",
            "   Доступ в инвентарь осуществляется нажатием клавиши E.",
            "   Посмотреть амуницию персонажа - нажатием Q.",
            "   Предметы, находящиеся в руках используются нажатием левой и ",
            "правой кнопки мыши. При отсутствии предмета в ячейке используется",
            "предмет по умолчанию, например кулаки.",
            "   Нажатие средней кнопки мыши позволяет обыскать умершего",
            "противника или сундук. Сундук может быть заперт, в таком случае его",
            "необходимо предварительно открыть с помощью ключа.",
            "ИНВЕНТАРЬ:",
            "   Для выбора и перемещения предмета в другую ячейку используется",
            "левая кнопка мыши(ЛКМ).",
            "   Правая кнопка мыши(ПКМ) позволяет использовать предмет на себя.",
            "   Средняя кнопка мыши(СКМ) показывает описание предмета.",
            "   SHIFT + (ЛКМ) объединяет одинаковые предметы, за исключением",
            "предметов, для которых данная операция запрещена(оружие, амуниция).",
            "   CTRL + (ЛКМ) разделяет предметы"
        ]

    def _render(self):
        self._screen.fill(pygame.Color('BLACK'))
        self._render_central_string("HOTKEYS", color=pygame.Color('WHITE'), pos=(WIDTH // 2, 50))
        self._render_text(self.text, font=pygame.font.SysFont("MONOSPACE", 30),
                          color=pygame.Color("WHITE"), pos=(50, 100))
        pygame.display.flip()


class MenuScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.__menu_buttons_group = pygame.sprite.Group()
        self.__status = MENU_NONE
        self.__initialized = False

    def get_status(self):
        return self.__status

    def __init(self, game_exist):
        if not self.__initialized:
            buttons = [
                ("new_game.png", self.__new_game),
                ("continue_game.png", self.__continue_game),
                ("score_game.png", self.__score_game),
                ("HOTKEYS.png", self.__hotkeys_game),
                ("exit_game.png", self._terminate)
            ]
            if not game_exist:
                del buttons[1]
            pos = 100
            border = (HEIGHT - len(buttons) * pos) // 2
            for i, v in enumerate(buttons):
                button = Button(load_image(v[0], KEY_COLOR), v[1])
                button.rect.midtop = (WIDTH // 2, border + pos * i)
                self.__menu_buttons_group.add(button)
                self.__initialized = True

    def run_with_parameters(self, game_exist):
        self.__init(game_exist)
        super().run()

    def _render(self):
        self._screen.fill(pygame.Color('BLACK'))
        self.__menu_buttons_group.draw(self._screen)
        pygame.display.flip()

    def __clean(self):
        self.__menu_buttons_group.empty()
        self.__initialized = False

    def __new_game(self):
        self.__status = MENU_NEW_GAME
        self.stop()

    def __continue_game(self):
        self.__status = MENU_CONTINUE
        self.stop()

    def __score_game(self):
        self.__status = MENU_SCORE
        self.stop()

    def __hotkeys_game(self):
        self.__status = MENU_HOTKEYS
        self.stop()

    def stop(self):
        super().stop()
        self.__clean()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.__menu_buttons_group:
                    if btn.rect.collidepoint(event.pos):
                        btn.handle_click()


class ScoreTableScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.__text = [str(x) for x in [GameScore.title()] + GameScore.get(limit=15)]

    def run(self):
        self.__text = [str(x) for x in [GameScore.title()] + GameScore.get(limit=15)]
        super().run()

    def _render(self):
        self._screen.fill(pygame.Color('BLACK'))
        self._render_central_string("SCORE", color=pygame.Color('WHITE'), pos=(WIDTH // 2, 50))
        self._render_text(self.__text, font=pygame.font.SysFont("MONOSPACE", 30),
                          color=pygame.Color('WHITE'), pos=(20, 100))
        pygame.display.flip()


class CentralTextScreen(Screen):
    def __init__(self, screen, text):
        self.__text = text
        super().__init__(screen)

    def _render(self):
        self._screen.fill(pygame.Color('BLACK'))
        self._render_central_string(self.__text, color=pygame.Color('WHITE'), pos=(WIDTH // 2, HEIGHT // 2))
        pygame.display.flip()


class FailScreen(CentralTextScreen):
    def __init__(self, screen):
        super().__init__(screen, "Game Over")


class WinScreen(CentralTextScreen):
    def __init__(self, screen):
        super().__init__(screen, "Congratulations!")


class GameScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.__player = Player(3, 5)
        self.__levels = load_level_list()
        self.__game = Game()
        Game.add(self.__game)
        self.__current_level = 0
        self.__level = Level(self.__levels[self.__current_level], self.__player, self)
        camera.set_focus(self.__player)
        self.__level_complete = False
        self.__game_complete = False
        self.__player_dead = False

    def stop(self):
        super().stop()
        pygame.mixer.music.stop()

    def run(self):
        pygame.mixer.music.load("data/sounds/music.mp3")
        pygame.mixer.music.play(-1)
        super().run()

    def get_player(self):
        return self.__player

    def get_game_id(self):
        return self.__game.id

    def get_status(self):
        if self.__player_dead:
            return GAME_FAILED
        elif self.__game_complete:
            return GAME_COMPLETED
        elif not self.is_running():
            return GAME_PAUSED
        else:
            return GAME_RUNNING

    def death_delayed(self):
        if not self.__player_dead:
            self.__player_dead = True
            self._append_delayed_runners(DelayedRunner(90, self.stop))

    def next_level_delayed(self):
        if not self.__level_complete:
            self.__level_complete = True
            self._append_delayed_runners(DelayedRunner(90, self.__next_level))

    def __clean(self):
        self._clean_delayed_runners()
        self.__level.clean()

    def exit(self):
        self.__clean()
        self.__player.kill()
        self.__player.clean()
        self.stop()

    def __next_level(self):
        self.__level_complete = False
        self.__current_level += 1
        self.__clean()
        if self.__current_level >= len(self.__levels):
            self.__game_complete = True
            self.stop()
            return
        self.__level = Level(self.__levels[self.__current_level], self.__player, self)

    def _render(self):
        self._screen.fill(pygame.Color('BLACK'))

        landscape_group.draw(self._screen)
        corpse_group.draw(self._screen)
        obstacle_group.draw(self._screen)

        animated_obstacle_group.update(self._screen)
        creature_group.update(self._screen)

        window_groups.draw(self._screen)
        slots_group.update(self._screen)
        slots_group.draw(self._screen)
        items_group.draw(self._screen)
        buttons_group.draw(self._screen)
        items_group.update(self._screen)

        Slot.render_description(self._screen)

        self.__render_message()

        tick_counter.next()
        animation_tick_counter.next()

        pygame.display.flip()

    def __render_message(self):
        pos = (WIDTH // 2, HEIGHT // 2)
        if self.__player_dead:
            self._render_central_string("YOU ARE DEAD", color=pygame.Color('WHITE'),
                                        bg_color=pygame.Color('BLACK'), pos=pos)
        elif self.__level_complete:
            self._render_central_string("LEVEL COMPLETE", color=pygame.Color('WHITE'),
                                        bg_color=pygame.Color('BLACK'), pos=pos)

    def _handle_events(self):
        mouse.set_pos(pygame.mouse.get_pos())

        dx, dy = 0, 0
        obstacle = None
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
                self.stop()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [1, 2, 3]:
                    button = event.button
                    for i in chain(obstacle_group, corpse_group):
                        if camera.translate(i.rect).collidepoint(event.pos):
                            obstacle = i
                            break
                    for slot in slots_group:
                        if slot.rect.collidepoint(event.pos):
                            slot.handle_click(button, mods & pygame.KMOD_SHIFT, mods & pygame.KMOD_CTRL)
                            break
                    for btn in buttons_group:
                        if btn.rect.collidepoint(event.pos):
                            btn.handle_click()
                            break
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    Slot.clean_description()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    self.__player.get_inventory().handle_click(True)
                if event.key == pygame.K_q:
                    self.__player.get_ammunition().handle_click()
                if event.key == pygame.K_ESCAPE:
                    self.stop()
                if event.key == pygame.K_EQUALS:
                    vol = pygame.mixer.music.get_volume()
                    vol += 0.1
                    pygame.mixer.music.set_volume(vol)
                if event.key == pygame.K_MINUS:
                    vol = pygame.mixer.music.get_volume()
                    vol -= 0.1
                    pygame.mixer.music.set_volume(vol)

        if obstacle:
            if not self.__player.handle_click(obstacle, button):
                self.__player.step(dx, dy)
                camera.follow()
        else:
            self.__player.step(dx, dy)
            camera.follow()
