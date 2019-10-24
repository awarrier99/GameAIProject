from util import in_sight
import math
import pygame
from Workers import Workers


class Ray:

    def __init__(self, is_sweeping, cb, ecb):
        self.is_sweeping = is_sweeping
        self.angle_offset = 0
        self.offset_inc = True
        self.sweep_speed = 1
        self._resolved = True
        self.cb = cb
        self.ecb = ecb

    def get_collision(self, player, range_, sprites, walls):
        zone = player.rect.inflate(range_, range_)
        collidables = [sprite.rect for sprite in sprites]
        args = (player.loc, zone, player.direction, range_, collidables, walls)
        Workers.delegate(in_sight, args, callback=self.cb, error_callback=self.ecb)

    def draw(self, loc, dir, screen):
        yellow = 255, 255, 102
        l3_p2 = loc.x + 700 * math.cos(math.radians(self.angle_offset + dir)), loc.y + 700 * math.sin(
            math.radians(self.angle_offset + dir))
        pygame.draw.line(screen, yellow, (loc.x, loc.y), l3_p2)

    def update(self, player):

        if self.angle_offset > player.fov / 2:
            self.offset_inc = False
        if self.angle_offset < -player.fov / 2:
            self.offset_inc = True

        if self.is_sweeping:
            if self.offset_inc:
                self.angle_offset += self.sweep_speed
            else:
                self.angle_offset -= self.sweep_speed