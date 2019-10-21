import pygame

from Grid import Grid
from util import Loc, Actions


class World:
    directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    actions = [getattr(Actions, k) for k in dict(vars(Actions)).keys() if k.find('_') == -1]

    def __init__(self, size, ppg):
        self.size = self.width, self.height = size
        self.grid = Grid(*size)
        self.ppg = ppg
        self.wall_list = None

    def to_pixels(self, grid_loc):
        return Loc((grid_loc.x * self.ppg) - int(self.ppg / 2), (grid_loc.y * self.ppg) - int(self.ppg / 2))

    def to_grids(self, pixel_loc):
        return Loc((pixel_loc.x + int(self.ppg / 2)) / self.ppg, (pixel_loc.y + int(self.ppg / 2)) / self.ppg)

    def update(self):
        pass

    def draw(self, screen):
        black = 0, 0, 0
        i = 0
        skip = 0
        while i <= self.width:
            pygame.draw.line(screen, black, (i, 0), (i, self.height))
            pygame.draw.line(screen, black, (0, i), (self.width, i))
            if skip == 20:
                skip = 1
            else:
                skip = 20
            i += skip

    def create_wall(self):
        x, y = pygame.mouse.get_pos()
        grid_x = x / 19
        grid_y = y / 19

        self.grid[grid_x][grid_y] = 'W'

    def move(self, obj, action):
        direction = World.directions[World.actions.index(action)]
        loc = self.to_grids(obj.loc)
        loc = Loc(loc.x + direction[0], loc.y + direction[1])
        obj.loc = self.to_pixels(loc)
