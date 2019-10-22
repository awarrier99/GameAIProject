from util import in_sight
from Workers import Workers


class Ray:
    def __init__(self, cb, ecb):
        self._resolved = True
        self.cb = cb
        self.ecb = ecb

    def get_collisions(self, player, range_, sprites, walls):
        if self._resolved:
            zone = player.rect.inflate(range_, range_)
            collidables = [sprite.rect for sprite in sprites]
            args = (player.loc, zone, player.direction, range_, collidables, walls)
            Workers.delegate(in_sight, args, callback=self.cb, error_callback=self.ecb)

    def get_closest_collision(self, sprites):
        pass

    def update(self):
        pass



