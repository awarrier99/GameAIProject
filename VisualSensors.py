import pygame
import math
import util

from util import GridLoc, Colors


class VisualSensors:

    def __init__(self, player, width, height):  # eventually take list of players
        self.player = player
        self.field_of_view = player.fov
        self.width = width
        self.height = height

    def update(self):
        pass

    def draw(self, screen, path, goal, collision_lines):
        i = 0
        skip = 0
        while i <= self.width:
            pygame.draw.line(screen, Colors.BLACK, (i, 0), (i, self.height))
            pygame.draw.line(screen, Colors.BLACK, (0, i), (self.width, i))
            if skip == util.ppg - 1:
                skip = 1
            else:
                skip = util.ppg - 1
            i += skip

        l1_p1 = self.player.loc.x + self.player.offset.x / 2, self.player.loc.y + self.player.offset.y / 2
        x1, y1 = l1_p1
        l1_p2 = x1 + 700 * math.cos(math.radians(self.field_of_view / 2 + self.player.direction)), y1 + 700 * math.sin(
            math.radians(self.field_of_view / 2 + self.player.direction))
        pygame.draw.line(screen, Colors.GREEN, l1_p1, l1_p2)
        # pygame.gfxdraw.line(screen, int(l1_p1[0]), int(l1_p1[1]), int(l1_p2[0]), int(l1_p2[1]), green)

        l2_p2 = x1 + 700 * math.cos(math.radians(-self.field_of_view / 2 + self.player.direction)), y1 + 700 * math.sin(
            math.radians(-self.field_of_view / 2 + self.player.direction))
        pygame.draw.line(screen, Colors.GREEN, l1_p1, l2_p2)
        # pygame.gfxdraw.line(screen, int(l2_p1[0]), int(l2_p1[1]), int(l2_p2[0]), int(l2_p2[1]), green)

        # l3_p2 = x1 + 700 * math.cos(math.radians(self.ray_cast_angle + self.player.direction)), y1 + 700 * math.sin(
        #     math.radians(self.ray_cast_angle + self.player.direction))
        # pygame.draw.line(screen, yellow, l1_p1, l3_p2)

        for loc in path:
            path_x = loc[1].x
            path_y = loc[1].y
            path_p = GridLoc(path_x, path_y).to_pixel()
            if loc[1] == goal:
                pygame.draw.rect(screen, Colors.RED, (path_p.x - util.ppg / 2, path_p.y - util.ppg / 2, util.ppg, util.ppg))
            else:
                pygame.draw.rect(screen, Colors.GREEN, (path_p.x - util.ppg / 2, path_p.y - util.ppg / 2, util.ppg, util.ppg))

        for line in collision_lines:
            pygame.draw.line(screen, Colors.GREEN, line[0], line[-1])
