class TickCounter:
    def __init__(self):
        self.__logic_tick_counter = 0

    def next(self):
        self.__logic_tick_counter += 1

    def check(self, mod):
        return self.__logic_tick_counter % mod == 0

    def get(self):
        return self.__logic_tick_counter
