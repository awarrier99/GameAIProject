import pygame
import math

from pygame.math import Vector2
from Ray import Ray


class Player(pygame.sprite.Sprite):

    # feet_walk = [pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_0.png'), pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_1.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_2.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_3.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_4.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_5.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_6.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_7.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_8.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_9.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_10.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_11.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_12.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_13.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_14.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_15.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_16.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_17.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_18.png'),pygame.image.load('PlayerSprites/Images/feet/walk/survivor-walk_19.png')]
    # rifle_walk = [pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_0.png'), pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_1.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_2.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_3.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_4.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_5.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_6.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_7.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_8.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_9.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_10.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_11.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_12.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_13.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_14.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_15.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_16.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_17.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_18.png'),pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_19.png'),]

    # for image in feet_walk:
    #     pygame.transform.scale(image, (150, 99))
    # for image in rifle_walk:
    #     pygame.transform.scale(image, (150, 99))

    # feet_offset = rifle_walk[0].get_height() / 3

    def __init__(self, location):
        #  init
        pygame.sprite.Sprite.__init__(self)
        self.health = 100
        self.image = pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_0.png')
        self.image = pygame.transform.scale(self.image, (50, 33))
        self.rect = self.image.get_rect()
        self.loc = location
        self.rect.center = (self.loc.x, self.loc.y)
        self.dirty = 0
        self.orig_image = self.image
        self.pos = Vector2(self.loc.x, self.loc.y)  # The original center position/pivot point.
        self.offset = Vector2(9.346, -2.72)  # We shift the sprite 50 px to the right.
        self.direction = 0  # degrees: 0º is facing right
        self._last_dir = 0
        self.fov = 65  # degrees

    def shoot(self, direction):
        pass
        #  shoot bullet

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.orig_image, -self.direction, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.direction)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=(self.loc.x, self.loc.y) + offset_rotated)

    def update(self):
        self.direction %= 360

        self.rect.x = self.loc.x
        self.rect.y = self.loc.y

        x, y = pygame.mouse.get_pos()
        dx = (x - self.loc.x) or 0.0000001
        dy = (y - self.loc.y)

        self.direction = math.degrees(math.atan(dy/dx))
        if dx < 0:
            self.direction += 180
        if not self.direction == self._last_dir:
            self.dirty = 1
            self.rotate()

