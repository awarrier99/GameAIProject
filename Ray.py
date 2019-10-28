from util import line_of_sight


class Ray:

    def get_collider(self, start, direction, collidables, walls):

        collisions = line_of_sight(start, direction, collidables, walls)
        if collisions:
            return collisions

