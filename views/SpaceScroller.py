from . import *
import time
import random

class SpaceScroller(View):
    def __init__(self):
        self.y = 32
        self.lasery = self.y
        self.vy = 0
        self.obs = []
        self.dt = 0.1
        self.collided = False
        self.length = 0
        self.color = random.randint(4,63)
        self.objspeed = -1.5

        self.framespeed = 100
        self.frames = []
        self.lasercounter = 0
        self.laserdrawer = 0

    def _clamp(self, value, _min, _max):
        return min(max(_min, value), _max)

    def render_frame(self):
        frame = Frame(grid=[[0 for x in range(9)] for y in range(9)])
        # draw spaceship
        yapprox = self._clamp(int(self.y / 8),0,7)
        frame.set_value((0,self._clamp(yapprox+1,0,8)), self.color)
        frame.set_value((0,yapprox), self.color)
        frame.set_value((1,yapprox), self.color)
        frame.set_value((0,self._clamp(yapprox-1,0,8)), self.color)

        if self.laserdrawer > 0:
            for i in range(2,9):
                frame.set_value((i, yapprox), 62)
        # draw asteroids
        for ob in self.obs:
            xap = int(ob[0]/8)
            yap = int(ob[1]/8)
            frame.set_value((self._clamp(xap,0,8),self._clamp(yap,0,8)), 2)


        return frame.copy()



    def apply_physics(self):
        # every frame self.length chance to spawn asteroid
        if random.random() < self.length:
            self.obs.append((63, 63*random.random()))

        cop = self.obs.copy()
        self.obs.clear()

        #if self.lasercounter > 10 and len(self.obs) > 0:
        #    self.lasercounter = 0
        #    self.laserdrawer = 15
        #    self.lasery = self.y

        self.lasercounter += 1
        self.laserdrawer -= 1

        for ob in cop:
            x = ob[0]+ self.objspeed * self.dt
            if abs(ob[1] - self.y) < 12 and self.lasercounter > 80:
                self.lasercounter = 0
                self.laserdrawer = 15
                self.lasery = self.y
            if abs(self.lasery - ob[1]) < 12 and self.laserdrawer > 0:
                continue
            if x < 16:
                if abs(ob[1] - self.y) < 24:
                    self.collided = True
                    return
                if x < 0:
                    continue
            self.obs.append((x,ob[1]))

        self.length += 0.0001
        self.vy += 0.1 * (random.random()-0.5)
        if len(self.obs) > 0:

            self.vy += 3*(self.obs[0][1]-self.y)

        self.vy = self._clamp(self.vy, -2.0, 2.0)
        self.y += self.vy * self.dt

    def compile(self):
        k = 0
        while not self.collided:
            #time.sleep(0.2)
            self.apply_physics()
            self.frames.append(self.render_frame())
            if k > 50000:
                break
