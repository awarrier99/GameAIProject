import pygame

from Grid import Grid
from util import Loc, Actions, lerp


class World:
    directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    actions = [getattr(Actions, k) for k in dict(vars(Actions)).keys() if k.find('_') == -1]

    def __init__(self, size, ppg):
        self.size = self.width, self.height = size
        self.ppg = ppg
        self.grid = Grid(int(self.width / self.ppg), int(self.height / self.ppg))
        self.wall_list = []
        self.move_frames = 7
        self.obj = None
        self.start_loc = None
        self.end_loc = None
        self.frame = None
        self.frames = range(self.move_frames)

    def to_pixels(self, grid_loc):
        return Loc((grid_loc.x * self.ppg) - int(self.ppg / 2), (grid_loc.y * self.ppg) - int(self.ppg / 2))

    def to_grids(self, pixel_loc):
        return Loc((pixel_loc.x + int(self.ppg / 2)) / self.ppg, (pixel_loc.y + int(self.ppg / 2)) / self.ppg)

    def update(self):
        if self.frame == self.move_frames:
            self.obj = self.frame = self.start_loc = self.end_loc = None
        if self.obj:
            print(self.frame, self.start_loc, self.end_loc)
            obj_loc = lerp(self.frame, self.frames, self.start_loc, self.end_loc)
            print(obj_loc)
            self.obj.loc = obj_loc
            self.frame += 1

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
        grid_x = x / self.ppg
        grid_y = y / self.ppg

        self.grid[grid_x][grid_y] = 'W'

    def move(self, obj, action):
        print(action)
        if not self.obj:
            direction = World.directions[World.actions.index(action)]
            self.obj = obj
            self.start_loc = obj.loc
            loc = self.to_grids(obj.loc)
            end_loc = Loc(loc.x + direction[0], loc.y + direction[1])
            self.end_loc = self.to_pixels(end_loc)
            self.frame = 0
