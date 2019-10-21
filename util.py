import pygame
import queue
from operator import itemgetter


class Actions:
    UL = 'Up Left'
    U = 'Up'
    UR = 'Up Right'
    L = 'Left'
    R = 'Right'
    DL = 'Down Left'
    D = 'Down'
    DR = 'Down Right'


class Keys:
    RIGHT = [pygame.K_RIGHT, pygame.K_d]
    LEFT = [pygame.K_LEFT, pygame.K_a]
    UP = [pygame.K_UP, pygame.K_w]
    DOWN = [pygame.K_DOWN, pygame.K_s]

    @classmethod
    def right(cls, keys):
        if type(keys) is tuple:
            return keys[cls.RIGHT[0]] or keys[cls.RIGHT[1]]
        else:
            return keys == cls.RIGHT[0] or keys == cls.RIGHT[1]

    @classmethod
    def upright(cls, keys):
        return cls.right(keys) and cls.up(keys)

    @classmethod
    def downright(cls, keys):
        return cls.right(keys) and cls.down(keys)

    @classmethod
    def left(cls, keys):
        if type(keys) is tuple:
            return keys[cls.LEFT[0]] or keys[cls.LEFT[1]]
        else:
            return keys == cls.LEFT[0] or keys == cls.LEFT[1]

    @classmethod
    def upleft(cls, keys):
        return cls.left(keys) and cls.up(keys)

    @classmethod
    def downleft(cls, keys):
        return cls.left(keys) and cls.down(keys)

    @classmethod
    def up(cls, keys):
        if type(keys) is tuple:
            return keys[cls.UP[0]] or keys[cls.UP[1]]
        else:
            return keys == cls.UP[0] or keys == cls.UP[1]

    @classmethod
    def down(cls, keys):
        if type(keys) is tuple:
            return keys[cls.DOWN[0]] or keys[cls.DOWN[1]]
        else:
            return keys == cls.DOWN[0] or keys == cls.DOWN[1]


class Loc:
    def __init__(self, x, y):
        self.__x = int(x)
        self.__y = int(y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        return 'Loc({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        if not other or type(other) is not Loc:
            return False

        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y


class Node:
    def __init__(self, loc, action=None, cost=0.0, parent=None):
        self.loc = loc
        self.action = action
        self.cost = cost
        self.parent = parent
        self._is_wall = False

    def is_wall(self):
        return self._is_wall

    def __str__(self):
        return '{}{}'.format('W' if self.is_wall() else 'N', str(self.loc))

    def __repr__(self):
        return '{}{}'.format('Wall' if self.is_wall() else 'Node', repr(self.loc))

    def __eq__(self, other):
        if not other or type(other) is not Node:
            return False

        return self.loc == other.loc

    def __lt__(self, other):
        return self.loc.x < other.loc.x and self.loc.y < other.loc.y

    def __hash__(self):
        return hash((self.loc, self.is_wall()))


class Wall(Node):
    def __init__(self, loc):
        super().__init__(loc)
        self._is_wall = True


class PriorityQueue:
    def __init__(self):
        self._pq = queue.PriorityQueue()

    def push(self, item, priority):
        self._pq.put((priority, item))

    def pop(self):
        if not self._pq.empty():
            return self._pq.get()[1]
        return None


def dist(a, b):
    if type(a) is Node and type(b) is Node:
        dx = abs(a.loc.x - b.loc.x)
        dy = abs(a.loc.y - b.loc.y)
    elif type(a) is Loc and type(b) is Loc:
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
    else:
        raise ValueError('a ({}) and b ({}) type mismatch or not one of Node or Loc'.format(type(a), type(b)))

    return ((dx ** 2) + (dy ** 2)) ** 0.5


def euclidean_heuristic(node, goal):
    return dist(node, goal)


def pathfind(grid, start, end, heuristic=euclidean_heuristic):
    nodes = PriorityQueue()
    visited = set()

    current = start

    while not current == end:
        if current not in visited:
            visited.add(current)
            for neighbor in grid.neighbors(current):
                neighbor.parent = current
                neighbor.cost += current.cost

                priority = neighbor.cost
                if heuristic:
                    priority += heuristic(neighbor, end)
                nodes.push(neighbor, priority)

        current = nodes.pop()

    path = []
    curr = current
    while curr.parent is not None:
        path.insert(0, (curr.action, curr.loc))
        curr = curr.parent

    return path


def lerp(t, times, start, end):
    tmin, tmax = min(times), max(times)
    dt = (t - tmin) / (tmax - tmin)

    return Loc(dt * (end.x - start.x) + start.x, dt * (end.y - start.y) + start.y)
