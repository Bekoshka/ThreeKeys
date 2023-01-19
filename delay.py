from common import tick_counter


class DelayedRunner:
    def __init__(self, interval, callback):
        self.start = tick_counter.get()
        self.interval = interval
        self.callback = callback

    def check(self):
        if self.start + self.interval == tick_counter.get():
            self.callback()
