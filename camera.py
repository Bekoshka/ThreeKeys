from settings import WIDTH, HEIGHT


class Camera:
    def __init__(self, focus):
        self.__focus = focus
        self.__dx = 0
        self.__dy = 0

    def get_focus_pos(self):
        return self.__focus.rect.center

    def set_focus(self, focus):
        self.__focus = focus

    def follow(self):
        self.__dx = -(self.__focus.rect.x + self.__focus.rect.w // 2 - WIDTH // 2)
        self.__dy = -(self.__focus.rect.y + self.__focus.rect.h // 2 - HEIGHT // 2)

    def translate(self, rect):
        copy = rect.copy()
        copy.x += self.__dx
        copy.y += self.__dy
        return copy


camera = Camera(None)
