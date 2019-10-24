from util import in_sight
import math
import pygame
from Workers import Workers


class Ray:

    def __init__(self, cb, ecb):
        self._resolved = True
        self.wcb = cb
        self.ecb = ecb

    def draw(self, loc, dir, screen):
        pass

    def update(self, player):
        pass

    def cb(self, result):
        self._resolved = True
        self.wcb(result)

    def get_collision(self, player, sprites, walls):
        if self._resolved:
            self._resolved = False
            collidables = [sprite.rect for sprite in sprites]
            args = (player.loc, player.fov, player.direction, collidables, walls)
            Workers.delegate(in_sight, args, callback=self.cb, error_callback=self.ecb)

