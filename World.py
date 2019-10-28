import pygame
import settings
import random

from Grid import Grid
from util import PixelLoc, GridLoc, Colors, line_length, Loc
from traceback import print_exception
from Collider import Collider
from Gun import Pistol, SubMachine1, SubMachine2, AssualtRifle1, AssualtRifle2


class World:
    def __init__(self, player):
        self.grid = Grid(int(settings.width / settings.ppg), int(settings.height / settings.ppg))
        self.actions = []
        self.path = []
        self.draw_path = []
        self.goal_loc = None if settings.ai_mode else GridLoc(10, 10)
        self.last_goal = self.goal_loc
        self.player = player
        self.player.set_grid(self.grid)
        self.player.wcb = self.scan_callback
        self.player.ecb = World.task_error_callback
        self.wall_rects = []
        self.new_wall_rects = []
        self.old_wall_rects = []
        self.wall_thickness = 6
        self.guns = []
        self.sprites = pygame.sprite.Group(self.guns)

        locs = [(5, 5), (8, 5), (4, 6), (3, 5)]
        self.colliders = [Collider(GridLoc(*loc).to_pixel()) for loc in locs]
        self.collision_lines = []

    def spawn_gun(self):
        gun_type = random.randint(1, 10)
        x = random.randint(0, self.grid.width)
        y = random.randint(0, self.grid.height)
        gun = None
        while self.grid[Loc(x, y)].is_wall():
            x = random.randint(0, self.grid.width)
            y = random.randint(0, self.grid.height)
        if gun_type == 1 or gun_type == 2 or gun_type == 3:
            gun = Pistol(GridLoc(x, y).to_pixel())
        elif gun_type == 4 or gun_type == 5:
            gun = SubMachine1(GridLoc(x, y).to_pixel())
        elif gun_type == 6 or gun_type == 7:
            gun = SubMachine2(GridLoc(x, y).to_pixel())
        elif gun_type == 8 or gun_type == 9:
            gun = AssualtRifle1(GridLoc(x, y).to_pixel())
        elif gun_type == 10:
            gun = AssualtRifle2(GridLoc(x, y).to_pixel())
        self.sprites.add(gun)
        self.guns.append(gun)

    def scan_callback(self, results):
        self.collision_lines = []
        for collidable, collision_line in results:
            if line_length(collision_line[0], collision_line[len(collision_line) - 1]) < 700:
                self.collision_lines.append(collision_line)

    @staticmethod
    def task_error_callback(err):
        print('Task failed')
        print_exception(type(err), err, None)

    def set_goal(self, x, y):
        self.last_goal = self.goal_loc
        self.goal_loc = PixelLoc(x, y).to_grid()

    def update(self):
        if len(self.guns) < 5:
            self.spawn_gun()
        for gun in self.guns:
            col = self.player.rect.colliderect(gun.rect)
            if col:
                self.player.gun = gun
                self.guns.remove(gun)
                self.sprites.remove(gun)

        self.player.scan(self.colliders, self.grid.walls)

    def toggle_ai(self):
        self.goal_loc = self.last_goal = None
        self.draw_path = []
        self.path = []
        if not settings.ai_mode:
            self.player.end_move(flush_queue=True, finish_interpolation=True)

    def toggle_pathfinding(self):
        self.goal_loc = None
        self.draw_path = []
        self.path = []

    def get_wall_action(self):
        mouse_loc = PixelLoc(*pygame.mouse.get_pos()).to_grid()
        return 'R' if mouse_loc in self.grid.walls else 'A'

    def create_wall(self, last_grid, wall_action):
        mouse_loc = PixelLoc(*pygame.mouse.get_pos()).to_grid()
        if not (last_grid == mouse_loc or self.player.loc.to_grid() == mouse_loc):
            if wall_action == 'A' and mouse_loc not in self.grid.walls:
                self.grid.add_wall(mouse_loc)
            elif wall_action == 'R' and mouse_loc in self.grid.walls:
                self.grid.remove_wall(mouse_loc)
        return mouse_loc

    def generate_wall_rects(self, walls):
        wall_rects = []
        for wall_center in walls:
            wall_p = wall_center.to_pixel()

            if self.grid[wall_center.add(GridLoc(0, -1))].is_wall():  # if there is a wall above this wall
                wall_rects.append(pygame.Rect(wall_p.x - self.wall_thickness / 2, wall_p.y - settings.ppg / 2,
                                              self.wall_thickness, settings.ppg / 2 + 1))
            if self.grid[wall_center.add(GridLoc(0, 1))].is_wall():  # if there is a wall below this wall
                wall_rects.append(pygame.Rect(wall_p.x - self.wall_thickness / 2, wall_p.y +
                                              self.wall_thickness / 2, self.wall_thickness, settings.ppg / 2 + 1))
            if self.grid[wall_center.add(GridLoc(-1, 0))].is_wall():  # if there is to the left of this wall
                wall_rects.append(pygame.Rect(wall_p.x - settings.ppg / 2, wall_p.y - self.wall_thickness / 2,
                                              settings.ppg / 2 + 1, self.wall_thickness))
            if self.grid[wall_center.add(GridLoc(1, 0))].is_wall():  # if there is to the left of this wall
                wall_rects.append(pygame.Rect(wall_p.x + self.wall_thickness / 2, wall_p.y -
                                              self.wall_thickness / 2, settings.ppg / 2 + 1, self.wall_thickness))

            wall_rects.append(pygame.Rect(wall_p.x - self.wall_thickness / 2, wall_p.y - self.wall_thickness / 2,
                                          self.wall_thickness, self.wall_thickness))

        return wall_rects

    def draw(self, screen, background):
        self.sprites.draw(screen)
        if settings.dirty_rects:
            new_walls = [w for w in self.grid.walls if w not in self.grid._last_walls]
            old_walls = [w for w in self.grid._last_walls if w not in self.grid.walls]
            self.new_wall_rects = self.generate_wall_rects(new_walls)
            self.old_wall_rects = self.generate_wall_rects(old_walls)
            self.grid._last_walls = self.grid.walls.copy()
        else:
            self.wall_rects = self.generate_wall_rects(self.grid.walls)

        if settings.dirty_rects:
            for rect in self.new_wall_rects:
                screen.fill(Colors.BLACK, rect)
            for rect in self.old_wall_rects:
                screen.blit(background, rect)
        else:
            for rect in self.wall_rects:
                screen.fill(Colors.BLACK, rect)
        self.player.draw(screen)
        return self.new_wall_rects, self.old_wall_rects

