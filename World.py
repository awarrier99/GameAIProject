import pygame

from Grid import Grid
from AI import AI
from util import Loc, Node, lerp, directions, actions, Queue
from traceback import print_exception


class World:
    def __init__(self, size, ppg, move_frames, ai_mode):
        self.size = self.width, self.height = size
        self.ppg = ppg
        self.grid = Grid(int(self.width / self.ppg), int(self.height / self.ppg))
        self.path = []
        self.__ai_mode = ai_mode
        self._ai_moving = False
        self.goal_loc = None if self.__ai_mode else Loc(10, 10)
        self.move_frames = move_frames or 12
        self.obj = None
        self.frame = 0
        self.start_loc = None
        self.end_loc = None
        self.frames = range(self.move_frames)
        self.player = None
        self.moves = Queue()
        self.count = 0
        self.ai = AI(self.grid, self.ai_callback, World.ai_error_callback)

    def ai_callback(self, result):
        self.path = result
        if self.__ai_mode and result:
            self._ai_moving = True
            self.move(self.player, result[0][0])
            for move in result[1:]:
                self.moves.push((self.player, move[0]))

    @staticmethod
    def ai_error_callback(err):
        print('AI Task failed')
        print_exception(type(err), err, None)

    def to_pixels(self, grid_loc):
        return Loc((grid_loc.x * self.ppg) + int(self.ppg / 2) + 1, (grid_loc.y * self.ppg) + int(self.ppg / 2) + 1)

    def to_grids(self, pixel_loc):
        return Loc(int(pixel_loc.x / self.ppg), int(pixel_loc.y / self.ppg))

    def update(self):
        if self.goal_loc and (not self._ai_moving):
            self.ai.pathfind(Node(self.to_grids(self.player.loc)), Node(self.goal_loc))

        if self.frame == self.frames[-1] + 1:
            self.obj = self.start_loc = self.end_loc = None
            self.frame = 0
            if not self.moves.empty():
                self.move(*self.moves.pop())
            else:
                self._ai_moving = False
        elif self.obj:
            obj_loc = lerp(self.frame, self.frames, self.start_loc, self.end_loc)
            self.obj.loc = obj_loc
            self.frame += 1
        else:
            if not self.moves.empty():
                self.move(*self.moves.pop())

    def move(self, obj, action):
        if not self.obj:
            direction = directions[actions.index(action)]
            if direction[0] and direction[1]:
                self.frames = range(int(self.move_frames * 1.6))
            else:
                self.frames = range(self.move_frames)
            loc = self.to_grids(obj.loc)
            end_loc = Loc(loc.x + direction[0], loc.y + direction[1])
            if not (self.grid[end_loc.x][end_loc.y].is_wall() or self.grid.is_blocked(Node(loc), direction)):
                self.obj = obj
                self.start_loc = obj.loc
                self.end_loc = self.to_pixels(end_loc)
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
