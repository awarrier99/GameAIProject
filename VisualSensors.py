import pygame
import math


class VisualSensors:

    def __init__(self, player):  # eventually take list of players
        self.player = player
        self.field_of_view = player.fov

    def update(self):
        pass

    def draw(self, screen):

        green = 0, 255, 0
        l1_p1 = self.player.loc.x + self.player.offset.x / 2, self.player.loc.y + self.player.offset.y
        x1, y1 = l1_p1
        l1_p2 = x1 + 700 * math.cos(math.radians(self.field_of_view / 2 + self.player.direction)), y1 + 700 * math.sin(
            math.radians(self.field_of_view / 2 + self.player.direction))
        pygame.draw.line(screen, green, l1_p1, l1_p2)

        l2_p1 = self.player.loc.x + self.player.offset.x / 2, self.player.loc.y + self.player.offset.y
        x1, y1 = l1_p1
        l2_p2 = x1 + 700 * math.cos(math.radians(-self.field_of_view / 2 + self.player.direction)), y1 + 700 * math.sin(
            math.radians(-self.field_of_view / 2 + self.player.direction))
        pygame.draw.line(screen, green, l2_p1, l2_p2)