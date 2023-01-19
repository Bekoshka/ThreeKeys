from common import tick_counter


class DelayedRunner:
    def __init__(self, interval, callback):
        self.__start = tick_counter.get()
        self.__interval = interval
        self.__callback = callback

    def check(self):
        if self.__start + self.__interval == tick_counter.get():
            self.__callback()
