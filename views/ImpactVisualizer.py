import random
from .classes import *
import numpy as np


class ImpactVisualizer(AudioView):
    def __init__(self):
        self.framespeed = 32
        self.view_length = 320
        tmp = random.randint(12, 52)
        tmp2 = random.randint(20, 80)
        self.on_colors = random.choice([
            [[tmp for y in range(0, 9)] for x in range(0, 9)],
            #[[tmp2 + x for y in range(0, 9)] for x in range(0, 9)],
            #[[tmp2 + y for y in range(0, 9)] for x in range(0, 9)],
            [[tmp2 + x - y for y in range(0, 9)] for x in range(0, 9)],
            [[tmp2 - x + y for y in range(0, 9)] for x in range(0, 9)],
            #[[random.randint(3, 127) for x in range(0, 9)]
            # for y in range(0, 9)]
            ])
        self.off_colors = [[0 for y in range(0, 9)] for x in range(0, 9)]
        self.static_matrix = [[0 for y in range(0, 9)] for x in range(0, 9)]
        #self.swell_matrix = [[2 for y in range(0, 9)] for x in range(0, 9)]
        self.amps = []
        self.avg_length = 32
        self.impact = 0

    def ins_get_avg(self, amp):
        if len(self.amps) >= self.avg_length:
            self.amps.pop(0)
        self.amps.append(amp)
        return sum(self.amps) / len(self.amps)

    def get_frame(self, _amp, four):
        amp = np.sum(np.abs(four[-2:-1]))
        #print(amp)
        frame = Frame(grid=[[0 for y in range(0, 9)]
                            for x in range(0, 9)], channel_grid=self.static_matrix)
        avg = self.ins_get_avg(amp)
        radius = 1.5 * amp / avg
        for x in range(0, 9):
            for y in range(0, 9):
                r_p = (x-4)**2 + (y-4)**2
                if r_p < radius**2:
                    frame.set_value((x, y), self.on_colors[x][y])
                    if r_p > 6:
                        frame.set_channel_value((x, y), 2)
        return frame
