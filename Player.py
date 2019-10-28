import pygame

from pygame.math import Vector2
from util import PixelLoc, get_direction, in_sight, Colors, end_points, Loc
from Workers import Workers
from Ray import Ray
from Gun import Pistol, SubMachine1, SubMachine2, AssualtRifle1, AssualtRifle2


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
        self.image = pygame.image.load('PlayerSprites/Images/handgun/move/survivor-move_handgun_0.png')
        self.image = pygame.transform.scale(self.image, (50, 33))
        self.rect = self.image.get_rect()
        self.loc = location
        self.last_loc = location
        self.rect.center = self.loc.as_tuple()
        self.dirty = 0
        self.orig_image = self.image
        self.offset = Vector2(9.346, -2.72)  # We shift the sprite 50 px to the right.
        self.direction = 0  # degrees: 0º is facing right
        self._last_dir = 0
        self.view_distance = 700
        self.fov = 65  # degrees
        self._resolved = True
        self.wcb = None
        self.ecb = None
        self.sensor_range = 150
        self.sensor_circle = pygame.Rect(0, 0, self.sensor_range, self.sensor_range)
        self.sensor_reset_time = 0
        self.shooting = False
        self.bullet_time = 5
        self.gun = Pistol(Loc(0, 0))
        self.prev_gun = None
        self.shoot_delay = self.gun.fire_delay

    def cb(self, result):
        self._resolved = True
        self.wcb(result)

    def shoot(self, sprites, walls):
        if self.shoot_delay < 0 < self.gun.ammo:
            ray = Ray()
            collidables = [sprite.rect for sprite in sprites]
            ray.get_collider(self.loc, self.direction, collidables, walls)
            self.gun.ammo -= 1
            self.sensor_range = 400
            self.sensor_reset_time = 10
            self.shoot_delay = self.gun.fire_delay
            self.bullet_time = 5

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.orig_image, -self.direction, 1)
        offset_rotated = self.offset.rotate(self.direction)
        self.rect = self.image.get_rect(center=self.loc.as_tuple() + offset_rotated)

    def scan(self, sprites, walls):
        if self._resolved:
            self._resolved = False
            collidables = [sprite.rect for sprite in sprites]
            # sprite_map = {s.rect: s for s in sprites}
            args = (self.loc, self.fov, self.direction, collidables, walls)
            Workers.delegate(in_sight, args, callback=self.cb, error_callback=self.ecb)

    def update(self):
        if self.prev_gun is not self.gun:
            if self.gun is type(Pistol):
                self.image = pygame.image.load('PlayerSprites/Images/handgun/move/survivor-move_handgun_0.png')
            elif self.gun is type(AssualtRifle1) or type(AssualtRifle2):
                self.image = pygame.image.load('PlayerSprites/Images/rifle/move/survivor-move_rifle_0.png')
            elif self.gun is type(SubMachine2) or type(SubMachine1):
                self.image = pygame.image.load('PlayerSprites/Images/shotgun/move/survivor-move_shotgun_0.png')
            self.image = pygame.transform.scale(self.image, (50, 33))
            self.rect = self.image.get_rect()
            self.rect.center = self.loc.as_tuple()
            self.prev_gun = self.gun

        self.sensor_reset_time -= 1
        self.bullet_time -= 1
        self.shoot_delay -= 1
        if self.sensor_reset_time < 0:
            self.sensor_range = 150
        self.last_loc = PixelLoc(self.rect.x, self.rect.y)
        self.rect.x, self.rect.y = self.loc.as_tuple()
        self.sensor_circle.center = self.loc.as_tuple()
        x, y = pygame.mouse.get_pos()

        self.direction = get_direction(self.loc, PixelLoc(x, y))
        self.dirty = 1
        self.rotate()

    def draw(self, screen):

        if self.bullet_time > 0:
            pygame.draw.line(screen, Colors.YELLOW, (self.loc.x, self.loc.y), (end_points((self.loc.x, self.loc.y), self.direction, 1000)))

        # pygame.draw.rect(screen, Colors.WHITE, (self.loc.x - self.sensor_range, self.loc.y - self.sensor_range,
        #                                         self.sensor_range * 2, self.sensor_range * 2), 1)
