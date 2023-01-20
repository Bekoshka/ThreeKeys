import pygame

from screen import StartScreen, GameScreen, FailScreen, WinScreen, ScoreTableScreen, MenuScreen, HotkeysScreen
from settings import SIZE
from globals import GAME_PAUSED, GAME_FAILED, GAME_COMPLETED, MENU_SCORE, MENU_NEW_GAME, MENU_HOTKEYS


def main_loop():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    screen = pygame.display.set_mode(SIZE)  # , pygame.FULLSCREEN)

    start = StartScreen(screen)
    fail = FailScreen(screen)
    win = WinScreen(screen)
    game = None
    menu = MenuScreen(screen)
    start.run()
    while True:
        while True:
            menu.run(bool(game))
            status = menu.get_status()
            if status == MENU_SCORE:
                ScoreTableScreen(screen).run()
                continue
            elif status == MENU_NEW_GAME:
                if game:
                    game.exit()
                game = GameScreen(screen)
            elif status == MENU_HOTKEYS:
                HotkeysScreen(screen).run()
                continue
            game.run()
            status = game.get_status()
            if status == GAME_PAUSED:
                continue
            break
        if status == GAME_FAILED:
            fail.run()
        elif status == GAME_COMPLETED:
            win.run()
        game.exit()
        game = None


if __name__ == '__main__':
    main_loop()
