import pygame
import math
import util

from util import Loc, to_pixels


class VisualSensors:

    def __init__(self, player, width, height):  # eventually take list of players
        self.player = player
        self.field_of_view = player.fov
        self.width = width
        self.height = height

    def update(self):
        pass

    def draw(self, screen, path, goal, collision_lines):
        black = 0, 0, 0
        green = 0, 255, 0
        yellow = 255, 255, 102
        red = 255, 0, 0

        i = 0
        skip = 0
        while i <= self.width:
            pygame.draw.line(screen, black, (i, 0), (i, self.height))
            pygame.draw.line(screen, black, (0, i), (self.width, i))
            if skip == util.ppg - 1:
                skip = 1
            else:
                skip = util.ppg - 1
            i += skip

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

        # l3_p2 = x1 + 700 * math.cos(math.radians(self.ray_cast_angle + self.player.direction)), y1 + 700 * math.sin(
        #     math.radians(self.ray_cast_angle + self.player.direction))
        # pygame.draw.line(screen, yellow, l1_p1, l3_p2)

        for loc in path:
            path_x = loc[1].x
            path_y = loc[1].y
            path_p = to_pixels(Loc(path_x, path_y))
            if loc[1] == goal:
                pygame.draw.rect(screen, red, (path_p.x - util.ppg / 2, path_p.y - util.ppg / 2, util.ppg, util.ppg))
            else:
                pygame.draw.rect(screen, green, (path_p.x - util.ppg / 2, path_p.y - util.ppg / 2, util.ppg, util.ppg))

        for line in collision_lines:
            pygame.draw.line(screen, green, line[0], line[-1])
