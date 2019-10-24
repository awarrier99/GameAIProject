import pygame
import math
import util

from util import Colors


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

        l2_p2 = x1 + 700 * math.cos(math.radians(-self.field_of_view / 2 + self.player.direction)), y1 + 700 * math.sin(
            math.radians(-self.field_of_view / 2 + self.player.direction))
        pygame.draw.line(screen, Colors.GREEN, l1_p1, l2_p2)

        for loc in path:
            path_p = loc.to_pixel()
            if loc == goal:
                pygame.draw.rect(screen, Colors.RED, (path_p.x - util.ppg / 2, path_p.y - util.ppg / 2, util.ppg, util.ppg))
            else:
                pygame.draw.rect(screen, Colors.GREEN, (path_p.x - util.ppg / 2, path_p.y - util.ppg / 2, util.ppg, util.ppg))

        for line in collision_lines:
            pygame.draw.line(screen, Colors.LIGHT_BLUE, line[0], line[-1])
