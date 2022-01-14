from . import *


class RadialWave(View):
    def __init__(self):
        self.frames = []
        self.size = 0
        self.iters = 3
        self.speed = 1.2
        self.dt = 0.1
        self.framespeed = 30
        self.color_period = 0.1
        self.color_offset = 0.2
        self.bh_size = 0

    def expected_length(self):
        return 10

    def description(self):
        return "Colorful radial wave"

    def settings(self):
        return {}

    def _clamp(self, value, _min, _max):
        return min(max(_min, value), _max)

    def compile(self):
        for i in range(0, self.iters):
            self.color_offset = 0.25*random.random()+0.25
            frame = Frame(grid=[[0 for x in range(9)] for y in range(9)], channel_grid=[
                          [0 for x in range(9)] for y in range(9)])
            while self.size < 8:
                for x in range(0, 9):
                    for y in range(0, 9):
                        if ((x-4)**2 + (y-4)**2 < self.size**2):
                            color = (127-3) * \
                                     self._clamp(self.color_offset + (self.color_period
                                                                      * ((x-4)**2 + (y-4)**2)/(self.size**2)), 0, 1) + 3
                            frame.set_value((x, y), int(color))
                            frame.set_channel_value(
                                (x, y), 2)  # pulsing effect
                self.size += self.speed * self.dt
                self.frames.append(frame.copy())

            while self.bh_size < 8:
                frame2 = frame.copy()
                for x in range(0, 9):
                    for y in range(0, 9):
                        if ((x-4)**2 + (y-4)**2 < self.bh_size ** 2):
                            frame2.set_value((x, y), 0)
                            frame2.set_channel_value((x, y), 2)
                self.bh_size += self.speed * self.dt
                self.frames.append(frame2.copy())
            self.size = 0
            self.bh_size = 0
