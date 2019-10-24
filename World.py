import pygame
import util

from Grid import Grid
from AI import AI
from util import PixelLoc, GridLoc, Node, lerp, directions, actions, Queue, ppg, Colors
from traceback import print_exception
from Ray import Ray
from Collider import Collider


class World:
    def __init__(self, player, size, move_frames, ai_mode, pathfinding, enable_dirty_rects):
        self.size = self.width, self.height = size
        self.grid = Grid(int(self.width / util.ppg), int(self.height / util.ppg))
        self.actions = []
        self.path = []
        self.draw_path = []
        self.__ai_mode = ai_mode
        self.__pathfinding = pathfinding
        self._ai_moving = False
        self._recompute = False
        self.goal_loc = None if self.__ai_mode else GridLoc(10, 10)
        self.last_goal = self.goal_loc
        self.frame_meta = {'obj': None, 'frame': 0, 'start': None, 'end': None, 'move_frames': move_frames,
                           'frames': range(move_frames)}
        self.player = player
        self.player.wcb = self.scan_callback
        self.player.ecb = World.task_error_callback
        self.moves = Queue()
        self._enable_dirty_rects = enable_dirty_rects
        self.wall_rects = []
        self.new_wall_rects = []
        self.old_wall_rects = []
        self.wall_thickness = 6

        self.ai = AI(self.grid, self.ai_callback, World.task_error_callback)

        locs = [(5, 5), (8, 5), (4, 6), (3, 5)]
        self.colliders = [Collider(GridLoc(*loc).to_pixel()) for loc in locs]
        self.collision_lines = []

    def ai_callback(self, result):
        self.actions = []
        self.path = []
        for r in result:
            self.actions.append(r[0])
            self.path.append(r[1])
        self.draw_path = self.path.copy()
        if self.__ai_mode and result:
            self._ai_moving = True
            self.move(self.player, self.actions[0])
            for move in self.actions[1:]:
                self.moves.push((self.player, move))

    def scan_callback(self, results):
        # pass
        self.collision_lines = []
        for collidable, collision_line in results:
            self.collision_lines.append(collision_line)

    @staticmethod
    def task_error_callback(err):
        print('Task failed')
        print_exception(type(err), err, None)

    def end_move(self, flush_queue=False, finish_interpolation=False):
        obj = self.frame_meta['obj']
        if flush_queue:
            self.moves.clear()
        if not finish_interpolation:
            if obj:
                obj.dirty = 0
            self.frame_meta['obj'] = self.frame_meta['start'] = self.frame_meta['end'] = None
            self.frame_meta['frame'] = 0

    def handle_ai_task(self):
        recompute = (not self.goal_loc == self.last_goal) or self._recompute
        if recompute:
            self._recompute = False
            self.end_move(flush_queue=True)

        find_path = False
        moved = (not self.player.loc == self.player.last_loc)
        if self.__ai_mode:
            if self.goal_loc and (not self._ai_moving or recompute):
                find_path = True
        elif self.__pathfinding and self.goal_loc and (not self.path or recompute or moved):
            find_path = True
        if find_path:
            self.ai.pathfind(Node(self.player.loc.to_grid()), Node(self.goal_loc))

    def set_goal(self, x, y):
        self.last_goal = self.goal_loc
        self.goal_loc = PixelLoc(x, y).to_grid()

    def update(self):
        self.player.scan(self.colliders, self.grid.walls)
        self.handle_ai_task()

        obj = self.frame_meta['obj']
        frame = self.frame_meta['frame']
        frames = self.frame_meta['frames']
        start = self.frame_meta['start']
        end = self.frame_meta['end']

        if frame == len(frames):
            self.end_move()

            if self._ai_moving:
                self.draw_path = self.draw_path[1:] if len(self.draw_path) > 1 else []
            if not self.moves.empty():
                self.move(*self.moves.pop())
            elif self._ai_moving:
                self._ai_moving = False
        elif obj:
            obj_loc = lerp(frame, frames, start, end)
            obj.loc = obj_loc
            self.frame_meta['frame'] += 1
        else:
            if not self.moves.empty():
                self.move(*self.moves.pop())

    def move(self, obj_, action):
        obj = self.frame_meta['obj']
        move_frames = self.frame_meta['move_frames']
        if not obj:
            direction = directions[actions.index(action)]
            if direction.x and direction.y:
                self.frame_meta['frames'] = range(int(move_frames * 1.6))
            else:
                self.frame_meta['frames'] = range(move_frames)
            loc = obj_.loc.to_grid()
            end_loc = loc.add(direction)
            if not self.grid[end_loc].is_wall():
                obj_.dirty = 1
                self.frame_meta['obj'] = obj_
                self.frame_meta['start'] = obj_.loc
                self.frame_meta['end'] = end_loc.to_pixel()
            elif self.__ai_mode:
                self._recompute = True
            else:
                loc1 = GridLoc(loc.x, end_loc.y)
                loc2 = GridLoc(end_loc.x, loc.y)
                node1 = self.grid[loc1]
                node2 = self.grid[loc2]
                if node1.is_wall() and (not node2.is_wall()):
                    obj_.dirty = 1
                    self.frame_meta['obj'] = obj_
                    self.frame_meta['start'] = obj_.loc
                    self.frame_meta['end'] = loc2.to_pixel()
                elif (not node1.is_wall()) and node2.is_wall():
                    obj_.dirty = 1
                    self.frame_meta['obj'] = obj_
                    self.frame_meta['start'] = obj_.loc
                    self.frame_meta['end'] = loc1.to_pixel()
        elif self.frame_meta['frame'] == len(self.frame_meta['frames']) - 2:
            self.moves.push((obj_, action))

    def toggle_ai(self):
        self.__ai_mode = not self.__ai_mode
        self.goal_loc = None
        self.draw_path = []
        self.path = []
        if self.__ai_mode:
            self.__pathfinding = True
        else:
            self.end_move(flush_queue=True, finish_interpolation=True)

    def create_wall(self, last_grid):
        mouse_loc = PixelLoc(*pygame.mouse.get_pos())
        grid_loc = mouse_loc.to_grid()
        if not (last_grid == grid_loc or self.player.loc.to_grid() == grid_loc):
            if grid_loc not in self.grid.walls:
                self.grid.add_wall(grid_loc)
            else:
                self.grid.remove_wall(grid_loc)
        return grid_loc

    def generate_wall_rects(self, walls):
        wall_rects = []
        for wall_center in walls:
            wall_p = wall_center.to_pixel()

            if self.grid[wall_center.add(GridLoc(0, -1))].is_wall():  # if there is a wall above this wall
                wall_rects.append(pygame.Rect(wall_p.x - self.wall_thickness / 2, wall_p.y - util.ppg / 2,
                                              self.wall_thickness, util.ppg / 2 + 1))
            if self.grid[wall_center.add(GridLoc(0, 1))].is_wall():  # if there is a wall below this wall
                wall_rects.append(pygame.Rect(wall_p.x - self.wall_thickness / 2, wall_p.y +
                                              self.wall_thickness / 2, self.wall_thickness, util.ppg / 2 + 1))
            if self.grid[wall_center.add(GridLoc(-1, 0))].is_wall():  # if there is to the left of this wall
                wall_rects.append(pygame.Rect(wall_p.x - util.ppg / 2, wall_p.y - self.wall_thickness / 2,
                                              util.ppg / 2 + 1, self.wall_thickness))
            if self.grid[wall_center.add(GridLoc(1, 0))].is_wall():  # if there is to the left of this wall
                wall_rects.append(pygame.Rect(wall_p.x + self.wall_thickness / 2, wall_p.y -
                                              self.wall_thickness / 2, util.ppg / 2 + 1, self.wall_thickness))

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
