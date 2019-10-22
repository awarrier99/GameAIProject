from util import in_sight


class Ray():

    def __init__(self):
        pass

    def get_collision(self, player, range_, sprites):
        collision = in_sight(player, player.direction, range_, sprites)
        if collision:
            return collision[1]
        else:
            return None

    def get_closest_collision(self, sprites):
        pass

    def update(self):
        pass



