from . import *


class Asteroids(View):
    def __init__(self):
        self.frames = []
        self.framespeed = 60
        self.length = 10 * self.framespeed
        self.grav = 1

        self.asteroids = []
        self.spawn_chance = 0.01  # every frames
        self.asteroid_mass = 10
        self.hit = -1
        self.center = 40
        self.dt = 0.1
        self.earth_size = 20
        self.tick = 0

    def _apply_physics(self):
        if random.random() < self.spawn_chance:
            self.asteroids.append({
                "x": random.choice([-50.0, 3.0, 68.0, 100.0]),
                "y": 32*random.random()+16,
                "vx": 7 * random.random()-4,
                "vy": 10 * random.random()-5,
                "col": random.randint(1, 126)})
        new_ast = []
        for ast in self.asteroids:
            if ast["x"] > 64 and ast["vx"] > 0:
                continue
            if ast["x"] < 0 and ast["vx"] < 0:
                continue
            if ast["y"] < 0 and ast["vy"] < 0:
                continue
            if ast["y"] > 64 and ast["vy"] > 0:
                continue
            if abs(ast["x"]-self.center) < 20 and abs(ast["y"]-self.center) < 20:
                self.hit = 100
                continue
            r2 = (ast["x"]-self.center)**2 + (ast["y"]-self.center)**2
            vx = ast["vx"] - self.dt * self.grav * \
                math.cos(ast["x"]-self.center) / (self.asteroid_mass * r2)
            vy = ast["vy"] - self.dt * self.grav * \
                math.sin(ast["y"]-self.center) / (self.asteroid_mass * r2)
            x = ast["x"] + vx * self.dt
            y = ast["y"] + vy * self.dt
            new_ast.append({"x": x, "y": y, "vx": vx,
                            "vy": vy, "col": ast["col"]})
        self.asteroids = new_ast
        self.tick += 1
        self.hit -= 1

    def render_frame(self):
        frame = Frame(grid=[[0 for x in range(9)] for y in range(9)])

        # render earth
        if int(self.tick / 50) % 2 == 0:
            col1 = 79
            col2 = 21
        else:
            col1 = 21
            col2 = 79
        # if self.hit > 0, render earth as yellow
        if self.hit > 0:
            col1 = 13
            col2 = 13
        #(3-5, 3-5)
        frame.set_value((3, 3), col1)
        frame.set_value((3, 4), col2)
        frame.set_value((3, 5), col1)
        frame.set_value((4, 3), col2)
        frame.set_value((4, 4), col1)
        frame.set_value((4, 5), col2)
        frame.set_value((5, 3), col1)
        frame.set_value((5, 4), col2)
        frame.set_value((5, 5), col1)

        # draw Asteroids
        for ast in self.asteroids:
            xapprox = int(ast["x"]/8)
            yapprox = int(ast["y"]/8)
            if xapprox > 8 or yapprox > 8:
                continue
            if xapprox < 0 or yapprox < 0:
                continue
            frame.set_value((xapprox, yapprox), ast["col"])

        return frame

    def compile(self):
        for i in range(0, self.length):
            self._apply_physics()
            self.frames.append(self.render_frame())
