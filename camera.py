from settings import WIDTH, HEIGHT


class Camera:
    def __init__(self, focus):
        self.focus = focus
        self.dx = 0
        self.dy = 0

    def follow(self):
        self.dx = -(self.focus.rect.x + self.focus.rect.w // 2 - WIDTH // 2)
        self.dy = -(self.focus.rect.y + self.focus.rect.h // 2 - HEIGHT // 2)

    def translate(self, rect):
        copy = rect.copy()
        copy.x += self.dx
        copy.y += self.dy
        return copy


camera = Camera(None)
