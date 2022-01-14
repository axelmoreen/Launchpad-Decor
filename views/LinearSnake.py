from . import *


class LinearSnake(View):
    def __init__(self):
        self.frames = []
        self.framespeed = 60
        self.direction = bool(random.choice([True, False]))
        self.start = random.randint(0, 4)
        self.max = 8
        self.add_color_mode = bool(random.choice([True, False]))
        if (self.add_color_mode):
            self.color_speed = 15
        self.breathe = bool(random.choice([True, False]))
        self.color = random.randint(1, 128)

    def description(self):
        return "Simple snake pattern"

    def settings(self):
        return {}

    def expected_length(self):
        return 2

    def compile(self):
        last_frame = EmptyFrame()
        self.frames.append(last_frame)
        # START POS
        # 0: top left
        # 1: top right
        # 2: bottom left
        # 3: bottom right

        # direction
        # True: Vertical
        # False: Horizontal

        # Operations in order:
        # Vertical top left: -y +x
        # Vertical top right -y -x
        # Vertical bottom left: +y +x
        # Vertical bottom right: +y -x
        # Horizontal top left: +x -y
        # Horizontal top right: -x -y
        # Horizontal bottom left: +x +y
        # Horizontal bottom right: -x +y
        if self.start == 0:
            pos = [0, self.max]
        elif self.start == 1:
            pos = [self.max, self.max]
        elif self.start == 2:
            pos = [0, 0]
        else:
            pos = [self.max, 0]

        frame = last_frame.copy()
        frame.set_value(tuple(pos), self.color)
        self.frames.append(frame)
        last_frame = frame

        dir = int(self.direction)
        notdir = int(not self.direction)
        primary = 1  # first operation
        secondary = 1  # second operation

        if pos[dir] == self.max:
            primary = -1
        if pos[notdir] == self.max:
            secondary = -1

        for i in range(0, (self.max+1)**2-1):
            pos[dir] += primary
            if pos[dir] < 0:
                pos[dir] = 0
                primary = 1
                pos[notdir] += secondary
            elif pos[dir] > self.max:
                pos[dir] = self.max
                primary = -1
                pos[notdir] += secondary

            if (self.add_color_mode):
                self.color = 1 + ((self.color + self.color_speed) % 127)
            frame = last_frame.copy()

            frame.set_value(tuple(pos), self.color)
            if self.breathe:
                frame.set_channel_value(tuple(pos), 2)
            self.frames.append(frame)
            last_frame = frame
