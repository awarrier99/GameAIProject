import pygame
from pygame import Vector2
import math


class Ray(pygame.sprite.Sprite):

    def __init__(self, loc, dir):
        pygame.sprite.Sprite.__init__(self)
        yellow = 255, 255, 102
        self.loc = loc
        self.dir = dir
        self.image = pygame.Surface((800, 1))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.center = (loc.x, loc.y)

        self.orig_image = self.image
        self.pos = Vector2(self.loc.x, self.loc.y)  # The original center position/pivot point.
        self.offset = Vector2(400, 0)  # We shift the sprite 50 px to the right.

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.orig_image, -self.dir, 1)
        offset_rotated = self.offset.rotate(self.dir)
        self.rect = self.image.get_rect(center=(self.loc.x, self.loc.y) + offset_rotated)

    def get_collisions(self, sprites):
        collisions = []
        for sprite in sprites:
            col = pygame.sprite.collide_rect(self, sprite)
            if col == true:
                collisions.append(sprite)
        return collisions

    def get_closest_collision(self, sprites):
        collisions = self.get_collisions(sprites)
        closest_sprite = None
        min_dist = 9999
        for sprite in collisions:
            dist = math.sqrt((sprite.rect.x - self.loc.x) ** 2 + (sprite.rect.y - self.loc.y) ** 2)
            if dist < min_dist:
                min_dist = dist
                closest_sprite = sprite

        return closest_sprite

    def update(self):
        self.rect.x = self.loc.x
        self.rect.y = self.loc.y

        self.rotate()


