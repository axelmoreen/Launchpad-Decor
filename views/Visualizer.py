from .classes import *
import soundcard as sc
from numpy.fft import fft
from numpy.fft import fftfreq
import numpy as np
import math


class Visualizer(AudioView):
    def __init__(self):
        self.framespeed = 128
        self.view_length = 2000
        self.sr = 44100
        self.block_size = 1024
        tmp = random.randint(3, 127)
        tmp2 = random.randint(4, 52)
        self.colors = random.choice([[72, 5, 60, 84, 96, 124, 13, 17, 87],
                                     [37, 38, 39, 41, 42, 47, 69, 49, 81],
                                     [tmp2 + i for i in range(0, 9)],
                                     [tmp for i in range(0, 9)]])
        # because of the log scale. can be used to modify shape
        self._groups = [64, 32, 16, 8, 4, 2, 2, 1, 1]
        self.groups = []
        k = 0
        for gr in self._groups:
            self.groups.append((k, k+gr))
            k += gr
        self.bins_per_dot = 7
        self.last_val = [[] for i in range(0, 9)]
        self.avg_length = 5

    def _clamp(self, value, _min, _max):
        return min(max(_min, value), _max)

    def ins_value_and_avg(self, x, value):
        if len(self.last_val[x]) >= self.avg_length:
            self.last_val[x].pop(0)

        self.last_val[x].append(value)
        return sum(self.last_val[x]) / len(self.last_val[x])

    def get_frame(self, amp, four):
        frame = Frame(grid=[[0 for x in range(9)] for y in range(9)])
        for x in range(0, 9):
            streng = np.abs(
                np.sum(four[1+self.groups[x][0]:1+self.groups[x][1]].real))
            val = self._clamp(
                int(150*(math.log10(10 + streng / self._groups[x])-1)), 0, 8)
            _val = max(val, int(self.ins_value_and_avg(x, val)))

            for y in range(0, _val):
                frame.set_value((8-x, y), self.colors[x])
        return frame
