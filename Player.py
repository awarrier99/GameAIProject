import pygame
import settings

from pygame.math import Vector2
from util import PixelLoc, GridLoc, get_direction, in_sight, lerp, Colors, actions, directions, Queue
from Workers import Workers


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
        self.last_loc = location
        self.rect.center = self.loc.as_tuple()
        self._bot = False
        self._grid = None
        self.moving = False
        self.moves = Queue()
        self.frame_meta = {'frame': 0, 'start': None, 'end': None, 'frames': range(settings.move_frames)}
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
        self.shoot_delay = 25

    def is_bot(self):
        return self._bot

    def set_grid(self, grid):
        self._grid = grid

    def cb(self, result):
        self._resolved = True
        self.wcb(result)

    def shoot(self):
        if self.shoot_delay < 0:
            self.sensor_range = 400
            self.sensor_reset_time = 10
            self.shoot_delay = 15

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.orig_image, -self.direction, 1)
        offset_rotated = self.offset.rotate(self.direction)
        self.rect = self.image.get_rect(center=self.loc.as_tuple() + offset_rotated)

    def scan(self, sprites, walls):
        if self._resolved:
            self._resolved = False
            collidables = [sprite.rect for sprite in sprites]
            args = (self.loc, self.fov, self.direction, collidables, walls)
            Workers.delegate(in_sight, args, callback=self.cb, error_callback=self.ecb)

    def move(self, action):
        if not self.moving:
            direction = directions[actions.index(action)]
            self.set_frames(direction)
            loc = self.loc.to_grid()
            end_loc = loc.add(direction)
            if not self._grid[end_loc].is_wall():
                self.init_move(end_loc.to_pixel())
            elif self.is_bot():
                self._recompute = True
            else:
                self.normalize_diagonal(loc, end_loc)
        elif self.frame_meta['frame'] == len(self.frame_meta['frames']):
            self.moves.push(action)

    def set_frames(self, direction):
        if direction.x and direction.y:
            self.frame_meta['frames'] = range(int(settings.move_frames * 1.6))
        else:
            self.frame_meta['frames'] = range(settings.move_frames)

    def init_move(self, end):
        self.moving = True
        self.dirty = 1
        self.frame_meta['start'] = self.loc
        self.frame_meta['end'] = end

    def normalize_diagonal(self, loc, end):
        loc1 = GridLoc(loc.x, end.y)
        loc2 = GridLoc(end.x, loc.y)
        node1 = self._grid[loc1]
        node2 = self._grid[loc2]
        if node1.is_wall() and (not node2.is_wall()):
            self.init_move(loc2.to_pixel())
        elif (not node1.is_wall()) and node2.is_wall():
            self.init_move(loc1.to_pixel())

    def update(self):
        self.handle_move_frame()

        self.sensor_reset_time -= 1
        self.shoot_delay -= 1
        if self.sensor_reset_time < 0:
            self.sensor_range = 150
        self.last_loc = PixelLoc(self.rect.x, self.rect.y)
        self.rect.x, self.rect.y = self.loc.as_tuple()
        self.sensor_circle.center = self.loc.as_tuple()
        x, y = pygame.mouse.get_pos()

        if self.is_bot():
            if self.goal:
                self.direction = get_direction(self.loc, self.goal.to_pixel())
        else:
            self.direction = get_direction(self.loc, PixelLoc(x, y))
        self.dirty = 1
        self.rotate()

    def handle_move_frame(self):
        frame = self.frame_meta['frame']
        frames = self.frame_meta['frames']
        start = self.frame_meta['start']
        end = self.frame_meta['end']

        if frame == len(frames):
            self.end_move()

            if self.is_bot() and self.moving:
                self.draw_path = self.draw_path[1:] if len(self.draw_path) > 1 else []
            if not self.moves.empty():
                self.move(self.moves.pop())
        elif self.moving and start and end:
            self.loc = lerp(frame, frames, start, end)
            self.frame_meta['frame'] += 1
        else:
            if not self.moves.empty():
                self.move(self.moves.pop())

    def end_move(self, flush_queue=False, finish_interpolation=False):
        if flush_queue:
            self.moves.clear()
        if not finish_interpolation:
            self.moving = False
            self.dirty = 0
            self.frame_meta['obj'] = self.frame_meta['start'] = self.frame_meta['end'] = None
            self.frame_meta['frame'] = 0

    def draw(self, screen):
        pygame.draw.rect(screen, Colors.WHITE, (self.loc.x - self.sensor_range, self.loc.y - self.sensor_range,
                                                self.sensor_range * 2, self.sensor_range * 2), 1)
