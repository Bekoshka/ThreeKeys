from ticker import TickCounter

animation_tick_counter = TickCounter()


class Animation:
    def __init__(self, name, images, mod, is_loop=False):
        self.name = name
        self.is_loop = is_loop
        self.is_pause = True
        self.mod = mod
        self.images = images
        self.images_idx = 0

    def tick(self):
        global animation_tick_counter
        image = self.images[self.images_idx]
        changed = False
        if not self.is_pause:
            if animation_tick_counter.check(self.mod):
                self.images_idx = (self.images_idx + 1) % len(self.images)
                changed = True
                if self.images_idx == 0:
                    if not self.is_loop:
                        self.is_pause = True
        return image, changed

    def start(self):
        self.is_pause = False

    def stop(self):
        self.is_pause = True
