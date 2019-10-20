import pygame

from Grid import Grid


class World:
    def __init__(self, size):
        self.size = self.width, self.height = size
        self.Grid = Grid(*size)


