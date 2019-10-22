import pygame

from Grid import Grid
from AI import AI
from util import Loc, Node, lerp, directions, actions, Queue
from traceback import print_exception
from Ray import Ray
from Collider import Collider


class World:
    def __init__(self, size, ppg, move_frames, ai_mode, enable_dirty_rects):
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
        self._enable_dirty_rects = enable_dirty_rects
        self.wall_rects = []
        self.new_wall_rects = []
        self.old_wall_rects = []
        self.wall_thickness = 6
        self.ai = AI(self.grid, self.ai_callback, World.ai_error_callback)
        self.rays = [Ray() for _ in range(1)]

        self.collider1 = Collider(self.to_pixels(Loc(5, 5)))
        self.collider2 = Collider(self.to_pixels(Loc(8, 5)))
        self.collider3 = Collider(self.to_pixels(Loc(4, 6)))
        self.collider4 = Collider(self.to_pixels(Loc(3, 5)))
        self.colliders = [self.collider1, self.collider2, self.collider3, self.collider4]

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
        for ray in self.rays:
            collision = ray.get_collision(self.player, 1000, self.colliders)

        if self.goal_loc and (not self._ai_moving):
            self.ai.pathfind(Node(self.to_grids(self.player.loc)), Node(self.goal_loc))

        if self.frame == self.frames[-1] + 1:
            self.obj.dirty = 0
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
            if not self.grid[end_loc.x][end_loc.y].is_wall():
                obj.dirty = 1
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

    def generate_wall_rects(self, walls):
        wall_rects = []
        for wall_center in walls:
            wall_x, wall_y = wall_center
            wall_p = self.to_pixels(Loc(wall_x, wall_y))
            if self.grid[wall_x][wall_y - 1].is_wall():  # if there is a wall above this wall
                wall_rects.append(pygame.Rect(wall_p.x - self.wall_thickness / 2, wall_p.y - self.ppg / 2,
                                              self.wall_thickness, self.ppg / 2 + 1))
            if self.grid[wall_x][wall_y + 1].is_wall():  # if there is a wall below this wall
                wall_rects.append(pygame.Rect(wall_p.x - self.wall_thickness / 2, wall_p.y +
                                              self.wall_thickness / 2, self.wall_thickness, self.ppg / 2 + 1))
            if self.grid[wall_x - 1][wall_y].is_wall():  # if there is to the left of this wall
                wall_rects.append(pygame.Rect(wall_p.x - self.ppg / 2, wall_p.y - self.wall_thickness / 2,
                                              self.ppg / 2 + 1, self.wall_thickness))
            if self.grid[wall_x + 1][wall_y].is_wall():  # if there is to the left of this wall
                wall_rects.append(pygame.Rect(wall_p.x + self.wall_thickness / 2, wall_p.y -
                                              self.wall_thickness / 2, self.ppg / 2 + 1, self.wall_thickness))

            wall_rects.append(pygame.Rect(wall_p.x - self.wall_thickness / 2, wall_p.y - self.wall_thickness / 2,
                                          self.wall_thickness, self.wall_thickness))

        return wall_rects

    def draw(self, screen, background):
        black = 0, 0, 0

        if self._enable_dirty_rects:
            new_walls = [w for w in self.grid.walls if w not in self.grid._last_walls]
            old_walls = [w for w in self.grid._last_walls if w not in self.grid.walls]
            self.new_wall_rects = self.generate_wall_rects(new_walls)
            self.old_wall_rects = self.generate_wall_rects(old_walls)
            self.grid._last_walls = self.grid.walls.copy()
        else:
            self.wall_rects = self.generate_wall_rects(self.grid.walls)

        if self.new_wall_rects:
            print('old', self.old_wall_rects)
            print('new', self.new_wall_rects)

        if self._enable_dirty_rects:
            for rect in self.new_wall_rects:
                screen.fill(black, rect)
            for rect in self.old_wall_rects:
                screen.blit(background, rect)
        else:
            for rect in self.wall_rects:
                screen.fill(black, rect)
        return self.new_wall_rects, self.old_wall_rects
