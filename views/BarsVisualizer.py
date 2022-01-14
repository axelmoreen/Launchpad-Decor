from .classes import *

import numpy as np
import math


class BarsVisualizer(AudioView):
    framespeed = 128

    def __init__(self):
        self.framespeed = 128
        self.view_length = 1280

        tmp = random.randint(3, 127)
        tmp2 = random.randint(4, 52)
        self.colors = random.choice([[72, 5, 60, 84, 96, 124, 13, 17, 87],
                                     [37, 38, 39, 41, 42, 47, 69, 49, 81],
                                     [tmp2 + i for i in range(0, 9)],
                                     [tmp for i in range(0, 9)]])
        # because of the log scale. can be used to modify shape
        self._groups = [1, 1, 1, 1, 2, 4, 8, 16, 32]
        self.groups = []
        k = 0
        for gr in self._groups:
            self.groups.append((k, k+gr))
            k += gr
        self.bins_per_dot = 7
        self.last_val = [[] for i in range(0, 9)]
        self.last_val2 = []
        self.avg_length = 5
        self.avg_length2 = 50

    def settings(self):
        return {}

    def expected_length(self):
        return 10

    def description(self):
        return "Classic audio visualizer"

    def _clamp(self, value, _min, _max):
        return min(max(_min, value), _max)

    def ins_value_and_avg(self, x, value):
        if len(self.last_val[x]) >= self.avg_length:
            self.last_val[x].pop(0)

        self.last_val[x].append(value)
        return sum(self.last_val[x]) / len(self.last_val[x])

    def ins_value2(self, value):
        if len(self.last_val2) >= self.avg_length2:
            self.last_val2.pop(0)

        self.last_val2.append(value)

    def avg2(self):
        return sum(self.last_val2) / len(self.last_val2)

    def get_frame(self, amp, four):
        frame = Frame(grid=[[0 for x in range(9)] for y in range(9)])
        mult = 100
        if len(self.last_val2) > 0:
            avg2 = self.avg2()
            if avg2 > 0:
                mult = 1/avg2
        for x in range(0, 9):
            streng = np.sum(
                np.abs(four[1+self.groups[x][0]:1+self.groups[x][1]].real))
            #val = self._clamp(
            #    int(150*(math.log10(10 + streng / self._groups[x])-1)), 0, 8)
            #print(streng/self._groups[x])
            #print(streng/self._groups[x])
            self.ins_value2(streng / self._groups[x])
            #print(streng / self._groups[x], mult)

            val = self._clamp(int(1.5 * mult*streng / self._groups[x]), 0, 8)
            #print(val)
            _val = max(val, int(self.ins_value_and_avg(x, val)))

            for y in range(0, _val):
                frame.set_value((x, y), self.colors[x])
        return frame
