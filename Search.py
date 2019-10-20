import math

class Search:

    def __init__(self, world):
        self.world = world

    def find_path(self, startNode, endNode):
        pass

    def get_waypoint(self):
        pass

    def get_heuristic(self, state, goalState):
        sx, sy = state
        ex, ey = goalState

        dx = sx - ex
        dy = sy - ey

        return math.sqrt(dx ** 2 + dy ** 2)






