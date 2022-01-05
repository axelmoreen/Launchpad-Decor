from . import *
import random
import math
import time
import copy


class Pong(View):
    def __init__(self):
        # BOUNDED BY (0,0) (64,64) !
        # Bricks are 8x8 large.
        self.frames = []
        self.xstart = random.randint(0, 65)
        self.v = 4
        self.startang = (math.pi * 3) + (math.pi/6 *(0.5-random.random()))
        self.bricks = [(x, y, random.randint(1, 127))
                       for y in range(4, 8) for x in range(0, 8)]

        self.x = self.xstart
        self.y = 10
        self.vx = self.v * math.cos(self.startang)
        self.vy = self.v * math.sin(self.startang)
        self.dt = 0.2
        self.framespeed = 500

    def _clamp(self, value, _min, _max):
        return min(max(_min, value), _max)

    def do_physics_update(self):
        # collisions check
        if self.x <= 0:
            self.vx = abs(self.vx)
        elif self.x >= 64:
            self.vx = -abs(self.vx)
        if self.y <= 0:
            self.vy = abs(self.vy)
        elif self.y >= 64:
            self.vy = -abs(self.vy)

        _bricks = self.bricks.copy()
        for br in _bricks:
            if br[0] * 8 < self.x and self.x < (br[0]+1) * 8:
                if br[1] * 8 < self.y and self.y < (br[1] + 1) * 8:
                    # inside of bricks
                    # TODO: make code check which edge! otherwise we will just reverse X and go down
                    self.vx = -self.vx
                    self.vy = -abs(self.vy)
                    self.bricks.remove(br)

        self.x += self.vx * self.dt
        self.y += self.vy * self.dt

    def render_frame(self):
        frame = Frame(grid=[[0 for x in range(9)] for y in range(9)])

        # render paddle
        xapprox = self._clamp(int(self.x / 8), 0, 7)
        yapprox = self._clamp(int(self.y / 8), 0, 7)

        frame.set_value((xapprox, 0), 3)  # 3 = color white
        frame.set_value((min(xapprox+1, 7), 0), 3)  # 3 = color white
        frame.set_value((max(0, xapprox-1), 0), 3)  # 3 = color white

        # render ball
        frame.set_value((xapprox, self._clamp(yapprox, 1, 7)), 3)

        # render bricks
        for brick in self.bricks:
            frame.set_value((brick[0], brick[1]), brick[2])

        return frame.copy()

    def compile(self):
        k = 0
        while len(self.bricks) > 0:
            self.do_physics_update()
            self.frames.append(self.render_frame())
            k += 1
            if k > 50000:
                break
