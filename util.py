import pygame
import queue
import math


directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
actions = ['Up Left', 'Up', 'Up Right', 'Left', 'Right', 'Down Left', 'Down', 'Down Right']


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
        return '{}({})'.format('Wall' if self.is_wall() else 'Node', repr(self.loc))

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


class Queue:
    def __init__(self):
        self.__q = queue.Queue()

    def empty(self):
        return self.__q.empty()

    def push(self, item):
        self.__q.put(item)

    def pop(self):
        if not self.__q.empty():
            return self.__q.get()
        return None


class PriorityQueue:
    def __init__(self):
        self.__pq = queue.PriorityQueue()

    def empty(self):
        return self.__pq.empty()

    def push(self, item, priority):
        self.__pq.put((priority, item))

    def pop(self):
        if not self.__pq.empty():
            return self.__pq.get()[1]
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

        if nodes.empty():
            break
        current = nodes.pop()

    if not current == end:
        return []
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


def in_sight(player, direction, range_, obstacles):
    line_of_sight = get_line(player.loc, direction, range_, 5)
    zone = player.rect.inflate(range_, range_)
    collidable_sprites = [sprite for sprite in obstacles]
    collidables = [sprite.rect for sprite in obstacles]  # to support indexing
    collisions = zone.collidelistall(collidables)
    for x in range(1, len(line_of_sight)):
        for ind in collisions:
            if collidables[ind].collidepoint(line_of_sight[x]):
                return collidables[ind], collidable_sprites[ind]
    return None


def get_line(start, direction, range_, step):
    # Setup initial conditions
    x1, y1 = start.x, start.y
    x2 = int(x1 + range_ * math.cos(math.radians(direction)))
    y2 = int(y1 + range_ * math.sin(math.radians(direction)))
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + step):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points
