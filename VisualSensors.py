import pygame
import math
from pygame import gfxdraw
from util import Loc

class VisualSensors:

    def __init__(self, player, to_pixels, ppg):  # eventually take list of players
        self.player = player
        self.field_of_view = player.fov
        self.ppg = ppg
        self.to_pixels = to_pixels
        self.ray_cast_angle = self.player.direction
        self.ray_cast_increasing = True

    def update(self):
        if self.ray_cast_angle > self.player.direction + self.field_of_view / 2:
            self.ray_cast_increasing = False
        if self.ray_cast_angle < self.player.direction - self.field_of_view / 2:
            self.ray_cast_increasing = True

        # if self.ray_cast_increasing:
        #     self.ray_cast_angle += 3
        # else:
        #     self.ray_cast_angle -= 3

        # self.ray_cast_angle -= 5

    def draw(self, screen, path, goal):
        green = 0, 255, 0
        yellow = 255, 255, 102
        red = 255, 0 ,0

        l1_p1 = self.player.loc.x + self.player.offset.x / 2, self.player.loc.y + self.player.offset.y / 2
        x1, y1 = l1_p1
        l1_p2 = x1 + 700 * math.cos(math.radians(self.field_of_view / 2 + self.player.direction)), y1 + 700 * math.sin(
            math.radians(self.field_of_view / 2 + self.player.direction))
        pygame.draw.line(screen, green, l1_p1, l1_p2)
        # pygame.gfxdraw.line(screen, int(l1_p1[0]), int(l1_p1[1]), int(l1_p2[0]), int(l1_p2[1]), green)

        l2_p2 = x1 + 700 * math.cos(math.radians(-self.field_of_view / 2 + self.player.direction)), y1 + 700 * math.sin(
            math.radians(-self.field_of_view / 2 + self.player.direction))
        pygame.draw.line(screen, green, l1_p1, l2_p2)
        # pygame.gfxdraw.line(screen, int(l2_p1[0]), int(l2_p1[1]), int(l2_p2[0]), int(l2_p2[1]), green)

        l3_p2 = x1 + 700 * math.cos(math.radians(self.ray_cast_angle + self.player.direction)), y1 + 700 * math.sin(
            math.radians(self.ray_cast_angle + self.player.direction))
        pygame.draw.line(screen, yellow, l1_p1, l3_p2)

        for loc in path:
            path_x = loc[1].x
            path_y = loc[1].y
            path_p = self.to_pixels(Loc(path_x, path_y))
            if loc[1] == goal:
                pygame.draw.rect(screen, red, (path_p.x - self.ppg / 2, path_p.y - self.ppg / 2, self.ppg, self.ppg))
            else:
                pygame.draw.rect(screen, green, (path_p.x - self.ppg / 2, path_p.y - self.ppg / 2, self.ppg, self.ppg))

