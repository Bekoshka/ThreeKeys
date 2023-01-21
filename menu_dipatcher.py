import pygame

from screen import StartScreen, GameScreen, FailScreen, WinScreen, ScoreTableScreen, MenuScreen, HotkeysScreen
from settings import SIZE
from globals import GAME_PAUSED, GAME_FAILED, GAME_COMPLETED, MENU_SCORE, MENU_NEW_GAME, MENU_HOTKEYS


class MenuDispatcher:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        self.__screen = pygame.display.set_mode(SIZE)  # , pygame.FULLSCREEN)
        self.__start = StartScreen(self.__screen)
        self.__fail = FailScreen(self.__screen)
        self.__win = WinScreen(self.__screen)
        self.__game = None
        self.__menu = MenuScreen(self.__screen)
        self.__hotkeys = HotkeysScreen(self.__screen)
        self.__score = ScoreTableScreen(self.__screen)

    def run(self):
        self.__start.run()
        while True:
            while True:
                self.__menu.run_with_parameters(bool(self.__game))
                status = self.__menu.get_status()
                if status == MENU_SCORE:
                    self.__score.run()
                    continue
                elif status == MENU_NEW_GAME:
                    if self.__game:
                        self.__game.exit()
                    self.__game = GameScreen(self.__screen)
                elif status == MENU_HOTKEYS:
                    self.__hotkeys.run()
                    continue
                self.__game.run()
                status = self.__game.get_status()
                if status == GAME_PAUSED:
                    continue
                break
            if status == GAME_FAILED:
                self.__fail.run()
            elif status == GAME_COMPLETED:
                self.__win.run()
            self.__game.exit()
            self.__game = None
