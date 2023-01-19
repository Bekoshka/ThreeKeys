from ticker import TickCounter

animation_tick_counter = TickCounter()


class Animation:
    def __init__(self, name, images, mod, is_loop=False):
        self.__name = name
        self.__is_loop = is_loop
        self.__pause = True
        self.__mod = mod
        self.__images = images
        self.__images_idx = 0

    def is_pause(self):
        return self.__pause

    def get_name(self):
        return self.__name

    def get_image(self):
        return self.__images[self.__images_idx]

    def tick(self):
        global animation_tick_counter
        image = self.__images[self.__images_idx]
        changed = False
        if not self.__pause:
            if animation_tick_counter.check(self.__mod):
                self.__images_idx = (self.__images_idx + 1) % len(self.__images)
                changed = True
                if self.__images_idx == 0:
                    if not self.__is_loop:
                        self.__pause = True
        return image, changed

    def start(self):
        self.__pause = False

    def stop(self):
        self.__pause = True
