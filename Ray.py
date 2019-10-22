from util import in_sight


class Ray():

    def __init__(self):
        pass

    def get_collisions(self, player, range_, sprites):
        collisions = in_sight(player, player.direction, range_, sprites)
        return collisions

    def get_closest_collision(self, sprites):
        pass

    def update(self):
        pass



