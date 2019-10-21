import pygame

from Grid import Grid
from util import Loc, Actions, pathfind, Node, lerp


class World:
    directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    actions = [getattr(Actions, k) for k in dict(vars(Actions)).keys() if k.find('_') == -1]

    def __init__(self, size, ppg):
        self.size = self.width, self.height = size
        self.ppg = ppg
        self.grid = Grid(int(self.width / self.ppg), int(self.height / self.ppg))
        self.path = []
        self.goal_loc = Loc(30, 20)
        self.move_frames = 7
        self.obj = None
        self.start_loc = None
        self.end_loc = None
        self.frame = None
        self.frames = range(self.move_frames)

    def to_pixels(self, grid_loc):
        return Loc((grid_loc.x * self.ppg) - int(self.ppg / 2), (grid_loc.y * self.ppg) - int(self.ppg / 2))

    def to_grids(self, pixel_loc):
        return Loc((int(pixel_loc.x / self.ppg)), int(pixel_loc.y / self.ppg))

    def update(self):

        self.path = pathfind(self.grid, Node(self.to_grids(self.player.loc)), Node(self.goal_loc))


>>>>>>> Stashed changes
        if self.frame == self.move_frames:
            self.obj = self.frame = self.start_loc = self.end_loc = None
        if self.obj:
            obj_loc = lerp(self.frame, self.frames, self.start_loc, self.end_loc)
            self.obj.loc = obj_loc
            self.frame += 1

    def draw(self, screen):
        black = 0, 0, 0
        green = 0, 255, 0
        i = 0
        skip = 0
        while i <= self.width:
            pygame.draw.line(screen, black, (i, 0), (i, self.height))
            pygame.draw.line(screen, black, (0, i), (self.width, i))
            if skip == self.ppg - 1:
                skip = 1
            else:
                skip = self.ppg - 1
            i += skip

        for wall_center in self.grid.walls:
            wall_x, wall_y = wall_center
            wall_p = self.to_pixels(Loc(wall_x + 1, wall_y + 1))
            pygame.draw.rect(screen, black, (wall_p.x - self.ppg / 2, wall_p.y - self.ppg / 2, self.ppg, self.ppg))

        for loc in self.path:
            path_x = loc[1].x
            path_y = loc[1].y
            path_p = self.to_pixels(Loc(path_x + 1, path_y + 1))
            pygame.draw.rect(screen, green, (path_p.x - self.ppg / 2, path_p.y - self.ppg / 2, self.ppg, self.ppg))

    def create_wall(self, last_grid):
        x, y = pygame.mouse.get_pos()
        grid_x = int(x / self.ppg)
        grid_y = int(y / self.ppg)
        if not last_grid == (grid_x, grid_y):
            if (grid_x, grid_y) not in self.grid.walls:
                self.grid[grid_x][grid_y] = 'W'
                self.grid.walls.append((grid_x, grid_y))
            else:
                self.grid[grid_x][grid_y] = 'N'
                self.grid.walls.remove((grid_x, grid_y))
        return grid_x, grid_y

    def move(self, obj, action):
<<<<<<< Updated upstream
=======
        print(action)
>>>>>>> Stashed changes
        if not self.obj:
            direction = World.directions[World.actions.index(action)]
            self.obj = obj
            self.start_loc = obj.loc
            loc = self.to_grids(obj.loc)
            end_loc = Loc(loc.x + direction[0], loc.y + direction[1])
            self.end_loc = self.to_pixels(end_loc)
            self.frame = 0
