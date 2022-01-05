import random
import copy


class Frame:
    def __init__(self, grid=[[0 for x in range(9)] for y in range(9)], channel_grid=[[0 for x in range(9)] for y in range(9)]):
        self.grid = grid
        self.channel_grid = channel_grid

    def set_channel_value(self, tup, channel):
        self.channel_grid[tup[0]][tup[1]] = channel

    def get_channel_value(self, tup):
        return self.channel_grid[tup[0]][tup[1]]

    def set_value(self, tup, color):
        self.grid[tup[0]][tup[1]] = color

    def add_value(self, tup, amount):
        self.grid[tup[0]][tup[1]] = 1 + \
            ((self.grid[tup[0][tup[1]]] + amount) % 127)

    def get_value(self, tup):
        return self.grid[tup[0]][tup[1]]

    def copy(self):
        return copy.deepcopy(self)


class EmptyFrame(Frame):
    pass


class View:
    def __init_(self):
        self.frames = []
        self.framespeed = 60

    def get_frame_length(self):
        return 0

    def get_frames(self):
        return []

    def compile(self):
        pass
