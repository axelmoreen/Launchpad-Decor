import random
from . import *


class Rain(View):
    def __init__(self):
        self.frames = []
        self.framespeed = 60

        self.droplets = []
        self.water_level = 0  # float to go from 0-9
        self.droplet_chance = 0.06
        self.fill_rate = 0.15

        self.color = random.randint(3, 127)
        self.speed = 3
        self.dt = 0.1

    def description(self):
        return "It's raining colors"

    def settings(self):
        return {}

    def expected_length(self):
        return 15

    def _apply_physics(self):
        if random.random() < self.droplet_chance:
            self.droplets.append((random.randint(0, 8), 8.99))

        cop = self.droplets.copy()
        self.droplets.clear()

        for drop in cop:
            if drop[1] < self.water_level:
                self.water_level += self.fill_rate
                continue

            self.droplets.append((drop[0], drop[1]-self.speed * self.dt))

    def render_frame(self):
        frame = Frame(grid=[[0 for x in range(9)] for y in range(9)])

        # water
        for y in range(0, int(self.water_level)):
            for x in range(0, 9):
                frame.set_value((x, y), self.color)

        if self.water_level < 8:
            dec = int(10*(self.water_level-int(self.water_level)))
            for x in range(0, 9):
                if 10*random.random() < dec and dec > 4:
                    frame.set_value((x, int(self.water_level)), self.color)

        for drop in self.droplets:
            frame.set_value(
                (drop[0], int(drop[1])), self.color)
            if int(drop[1]) < 7:
                frame.set_value((drop[0], int(drop[1])+1), self.color)

        return frame.copy()

    def compile(self):
        while self.water_level < 9:
            self._apply_physics()
            self.frames.append(self.render_frame())
