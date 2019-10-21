import pygame

from Grid import Grid
from util import Loc, pathfind, Node, lerp, directions, actions, Queue


class World:
    def __init__(self, size, ppg):
        self.size = self.width, self.height = size
        self.ppg = ppg
        self.grid = Grid(int(self.width / self.ppg), int(self.height / self.ppg))
        self.path = []
        self.goal_loc = Loc(30, 20)
        self.move_frames = 5
        self.obj = None
        self.frame = None
        self.start_loc = None
        self.end_loc = None
        self.frames = range(self.move_frames)
        self.player = None
        self.moves = Queue()
        self.count = 0

    def to_pixels(self, grid_loc):
        return Loc((grid_loc.x * self.ppg) + int(self.ppg / 2) + 1, (grid_loc.y * self.ppg) + int(self.ppg / 2) + 1)

    def to_grids(self, pixel_loc):
        return Loc(int(pixel_loc.x / self.ppg), int(pixel_loc.y / self.ppg))

    def update(self):
        if self.count > 20:
            # self.path = pathfind(self.grid, Node(self.to_grids(self.player.loc)), Node(self.goal_loc))
            self.count = 0
        self.count += 1

        if self.frame == self.move_frames:
            self.obj = self.frame = self.start_loc = self.end_loc = None
            if not self.moves.empty():
                self.move(*self.moves.pop())
        if self.obj:
            obj_loc = lerp(self.frame, self.frames, self.start_loc, self.end_loc)
            self.obj.loc = obj_loc
            self.frame += 1

    def move(self, obj, action):
        if not self.obj:
            direction = directions[actions.index(action)]
            loc = self.to_grids(obj.loc)
            end_loc = Loc(loc.x + direction[0], loc.y + direction[1])
            if not self.grid[end_loc.x][end_loc.y].is_wall() and loc.x < self.grid.width and loc.y < self.grid.height:
                self.obj = obj
                self.start_loc = obj.loc
                self.end_loc = self.to_pixels(end_loc)
                self.frame = 0
        elif self.frame == self.move_frames - 2:
            self.moves.push((obj, action))

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

    def draw(self, screen):
        black = 0, 0, 0
        green = 0, 255, 0
        red = 255, 0, 0
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
            wall_p = self.to_pixels(Loc(wall_x, wall_y))
            pygame.draw.rect(screen, black, (wall_p.x - self.ppg / 2, wall_p.y - self.ppg / 2, self.ppg, self.ppg))

        for loc in self.path:
            path_x = loc[1].x
            path_y = loc[1].y
            path_p = self.to_pixels(Loc(path_x, path_y))
            if loc[1] == self.goal_loc:
                pygame.draw.rect(screen, red, (path_p.x - self.ppg / 2, path_p.y - self.ppg / 2, self.ppg, self.ppg))
            else:
                pygame.draw.rect(screen, green, (path_p.x - self.ppg / 2, path_p.y - self.ppg / 2, self.ppg, self.ppg))
