class Animation:
    def __init__(self, name, images, mod, is_loop=False):
        self.name = name
        self.is_loop = is_loop
        self.is_pause = True
        self.mod = mod
        self.images = images
        self.images_idx = 0
        self.tick_counter = 0

    def tick(self):
        image = self.images[self.images_idx]
        changed = False
        if not self.is_pause:
            if self.tick_counter % self.mod == 0:
                self.images_idx = (self.images_idx + 1) % len(self.images)
                changed = True
                if self.images_idx == 0:
                    if not self.is_loop:
                        self.is_pause = True
        self.tick_counter += 1
        return image, changed

    def start(self):
        self.is_pause = False

    def stop(self):
        self.is_pause = True
