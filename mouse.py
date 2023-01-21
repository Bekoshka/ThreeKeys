class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, pos):
        self.x, self.y = pos
