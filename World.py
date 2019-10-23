import pygame

from Grid import Grid
from AI import AI
from util import GridLoc, Node, lerp, directions, actions, Queue, ppg, Colors
from traceback import print_exception
from Ray import Ray
from Collider import Collider


class World:
    def __init__(self, player, size, move_frames, ai_mode, pathfinding, enable_dirty_rects):
        self.size = self.width, self.height = size
        self.grid = Grid(int(self.width / ppg), int(self.height / ppg))
        self.path = []
        self.__ai_mode = ai_mode
        self.__pathfinding = pathfinding
        self._ai_moving = False
        self.goal_loc = None if self.__ai_mode else GridLoc(10, 10)
        self.move_frames = move_frames
        self.obj = None
        self.frame = 0
        self.start_loc = None
        self.end_loc = None
        self.frames = range(self.move_frames)
        self.player = player
        self.player.wcb = self.scan_callback
        self.player.ecb = World.task_error_callback
        self.moves = Queue()
        self.count = 0
        self._enable_dirty_rects = enable_dirty_rects
        self.wall_rects = []
        self.new_wall_rects = []
        self.old_wall_rects = []
        self.wall_thickness = 6

        self.ai = AI(self.grid, self.ai_callback, World.task_error_callback)
        # self.rays = [Ray(self.ray_callback, self.task_error_callback) for _ in range(1)]

        self.collider1 = Collider(GridLoc(5, 5).to_pixel())
        self.collider2 = Collider(GridLoc(8, 5).to_pixel())
        self.collider3 = Collider(GridLoc(4, 6).to_pixel())
        self.collider4 = Collider(GridLoc(3, 5).to_pixel())
        self.colliders = [self.collider1, self.collider2, self.collider3, self.collider4]
        # self.colliders = [self.collider2]

        self.collision_lines = []

    def ai_callback(self, result):
        self.path = result
        if self.__ai_mode and result:
            self._ai_moving = True
            self.move(self.player, result[0][0])
            for move in result[1:]:
                self.moves.push((self.player, move[0]))

    def scan_callback(self, results):
        # pass
        self.collision_lines = []
        for collidable, collision_line in results:
            self.collision_lines.append(collision_line)

    @staticmethod
    def task_error_callback(err):
        print('Task failed')
        print_exception(type(err), err, None)

    def update(self):
        # for ray in self.rays:
        #     ray.get_collision(self.player, self.colliders, self.grid.walls)
        self.player.scan(self.colliders, self.grid.walls)

        if self.__pathfinding and self.goal_loc and (not self._ai_moving):
            self.ai.pathfind(Node(self.player.loc.to_grid()), Node(self.goal_loc))

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
            loc = obj.loc.to_grid()
            end_loc = GridLoc(loc.x + direction[0], loc.y + direction[1])
            if not self.grid[end_loc.x][end_loc.y].is_wall():
                obj.dirty = 1
                self.obj = obj
                self.start_loc = obj.loc
                self.end_loc = end_loc.to_pixel()
        elif self.frame == self.move_frames - 2:
            self.moves.push((obj, action))

    def create_wall(self, last_grid):
        x, y = pygame.mouse.get_pos()
        grid_x = int(x / ppg)
        grid_y = int(y / ppg)
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
            wall_p = GridLoc(wall_x, wall_y).to_pixel()
            if self.grid[wall_x][wall_y - 1].is_wall():  # if there is a wall above this wall
                wall_rects.append(pygame.Rect(wall_p.x - self.wall_thickness / 2, wall_p.y - ppg / 2,
                                              self.wall_thickness, ppg / 2 + 1))
            if self.grid[wall_x][wall_y + 1].is_wall():  # if there is a wall below this wall
                wall_rects.append(pygame.Rect(wall_p.x - self.wall_thickness / 2, wall_p.y +
                                              self.wall_thickness / 2, self.wall_thickness, ppg / 2 + 1))
            if self.grid[wall_x - 1][wall_y].is_wall():  # if there is to the left of this wall
                wall_rects.append(pygame.Rect(wall_p.x - ppg / 2, wall_p.y - self.wall_thickness / 2,
                                              ppg / 2 + 1, self.wall_thickness))
            if self.grid[wall_x + 1][wall_y].is_wall():  # if there is to the left of this wall
                wall_rects.append(pygame.Rect(wall_p.x + self.wall_thickness / 2, wall_p.y -
                                              self.wall_thickness / 2, ppg / 2 + 1, self.wall_thickness))

            wall_rects.append(pygame.Rect(wall_p.x - self.wall_thickness / 2, wall_p.y - self.wall_thickness / 2,
                                          self.wall_thickness, self.wall_thickness))

        return wall_rects

    def draw(self, screen, background):
        if self._enable_dirty_rects:
            new_walls = [w for w in self.grid.walls if w not in self.grid._last_walls]
            old_walls = [w for w in self.grid._last_walls if w not in self.grid.walls]
            self.new_wall_rects = self.generate_wall_rects(new_walls)
            self.old_wall_rects = self.generate_wall_rects(old_walls)
            self.grid._last_walls = self.grid.walls.copy()
        else:
            self.wall_rects = self.generate_wall_rects(self.grid.walls)

        if self._enable_dirty_rects:
            for rect in self.new_wall_rects:
                screen.fill(Colors.BLACK, rect)
            for rect in self.old_wall_rects:
                screen.blit(background, rect)
        else:
            for rect in self.wall_rects:
                screen.fill(Colors.BLACK, rect)
        return self.new_wall_rects, self.old_wall_rects
