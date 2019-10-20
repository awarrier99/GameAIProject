import pygame


class Grid:
    def __init__(self, *size):
        self.size = self.width, self.height = size
        self._grid = [[0 for _ in range(self.height)] for _ in range(self.width)]

    def __getitem__(self, idx):
        return self._grid[idx]

    def __setitem__(self, idx, value):
        return self._grid[idx]

    def __str__(self):
        string = ''
        for i in range(self.height):
            for j in range(self.width):
                string += str(self._grid[j][i]) + '  '

            string = string[:-2]
            string += '\n'

        return string
