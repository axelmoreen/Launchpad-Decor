from . import *
from time import *
from datetime import datetime
import math
# Different from the other views because it needs to gotten in real time
# Analog clock


class Clock(View):
    def __init__(self):
        self.color = 3
        self.good_points = [0, 0.125, 0.25,0.375, 0.5, 0.625, 0.75, 0.875,0.9]

    def nearest_neighbor(self, val, array):
        best = 1000000 # change this?
        neighb = array[0]
        for _val in array:
            diff = abs(val-_val)
            if diff < best:
                neighb = _val
                best = diff

        return neighb

    def get_frame(self):
        frame = Frame(grid=[[0 for x in range(9)] for y in range(9)])
        eps = 5
        angEps = 0.5
        angFactor = 0.5  # higher the number the lower epsilon at the edges
        softEps = 0.3
        bord = random.randint(3,127)
        for x in range(0, 9):
            for y in range(0, 9):
                # outer rim
                if (x-4)**2 + (y-4)**2 > 16 - eps:
                    if (x-4)**2 + (y-4)**2 < 16 + eps:
                        frame.set_value((x, y), bord)
                    continue

                # hour hand
                now = datetime.now()
                hr = now.hour % 12
                min = now.minute
                #hr = 3
                #min = 30
                sec = now.second
                #print(str(hr) + " " + str(min) + " "+str(sec))
                hrAng = 2 * math.pi * self.nearest_neighbor(hr / 12, self.good_points)
                minAng = 2 * math.pi * self.nearest_neighbor(min / 60, self.good_points)
                secAng = 2 * math.pi * self.nearest_neighbor(sec / 60, self.good_points)
                #print(str(hrAng) + " "+str(minAng) + " "+str(secAng))
                # center at (4,4)
                ang = (-math.atan2(y-4, x-4)
                       + (5 * math.pi / 2)) % (2 * math.pi)

                #if abs(secAng - ang) < angEps/math.pow(((0.1+x-4)**2)+((y-4)**2), angFactor):
                #    if abs(secAng - ang) > softEps:
                #        frame.set_value((x,y), 7)
                #    else:
                #        frame.set_value((x, y), 5)

                if abs(minAng - ang) < angEps/math.pow((0.1+x-4)**2+(y-4)**2, angFactor):
                    if abs(minAng - ang) > softEps:
                        frame.set_value((x,y), 2)
                    else:
                        frame.set_value((x, y), 3)

                if abs(hrAng - ang) < angEps/math.pow((0.1+x-4)**2+(y-4)**2, angFactor) and (x-4)**2+(y-4)**2 < 6:
                    if abs(hrAng - ang) > softEps:
                        frame.set_value((x,y), 2)
                    else:
                        frame.set_value((x, y), 3)

                frame.set_value((4, 4), 3)

        return frame.copy()
