import pygame
import queue
import math
import settings


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


class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    LIGHT_BLUE = (0, 191, 255)


class Loc:
    def __init__(self, x, y):
        self.__x = int(x)
        self.__y = int(y)
        self._type = None

    def add(self, loc):
        x = self.x + loc.x
        y = self.y + loc.y
        if self.is_grid():
            return GridLoc(x, y)
        elif self.is_pixel():
            return PixelLoc(x, y)
        else:
            return Loc(x, y)

    def as_tuple(self):
        return self.x, self.y

    @classmethod
    def from_tuple(cls, t):
        return cls(*t)

    def is_grid(self):
        return self._type == 'Grid'

    def is_pixel(self):
        return self._type == 'Pixel'

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        if self._type:
            return '{}Loc({}, {})'.format(self._type, self.x, self.y)
        return 'Loc({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        if not other or type(other) is not type(self):
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


class GridLoc(Loc):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._type = 'Grid'

    def to_pixel(self):
        return PixelLoc((self.x * settings.ppg) + int(settings.ppg / 2) + 1,
                        (self.y * settings.ppg) + int(settings.ppg / 2) + 1)


class PixelLoc(Loc):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._type = 'Pixel'

    def to_grid(self):
        return GridLoc(int(self.x / settings.ppg), int(self.y / settings.ppg))


directions = [GridLoc(*d) for d in directions]


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

    def clear(self):
        while not self.empty():
            self.pop()

    def empty(self):
        return self.__q.empty()

    def push(self, item):
        self.__q.put(item)

    def pop(self):
        if not self.empty():
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
    elif isinstance(a, Loc) and isinstance(b, Loc):
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

    return PixelLoc(dt * (end.x - start.x) + start.x, dt * (end.y - start.y) + start.y)


def in_sight(obj_loc, obj_fov, obj_direction, collidables, walls):
    in_fov = []
    visible = []
    for collidable in collidables:
        points = [collidable.center, collidable.topleft, collidable.bottomleft, collidable.topright, collidable.bottomright]

        for pt in points:
            cur_direction = get_direction(obj_loc, PixelLoc(*pt))

            angle = abs(obj_direction - cur_direction)
            if angle <= (obj_fov / 2.0) or angle >= (360 - (obj_fov / 2.0)):
                in_fov.append(collidable)
                break

    for collidable in in_fov:
        col_loc = PixelLoc(*collidable.center)
        if obj_loc == col_loc:
            visible.append((collidable, create_line(obj_loc, obj_loc, 1)))
            continue
        collision_line = create_line(obj_loc, col_loc, 1)
        blocked = False
        for i in range(1, len(collision_line)):
            grid_loc = PixelLoc(*collision_line[i]).to_grid()
            if grid_loc in walls:
                blocked = True
                break
            for c in in_fov:
                if (not c == collidable) and c.collidepoint(collision_line[i]):
                    blocked = True
            if blocked:
                break
        if not blocked:
            visible.append((collidable, collision_line))

    return visible


def get_direction(start, end):
    dx = end.x - start.x
    dy = end.y - start.y

    direction = math.degrees(math.atan2(-dy, -dx)) + 180
    return direction


def create_line(start, end, step):
    points = []
    if start == end:
        return [start.as_tuple()]
    if end.x < start.x:
        t = end
        end = start
        start = t
    if end.x == start.x:
        ys = range(min(start.y, end.y), max(start.y, end.y))
        xs = [start.x for _ in ys]
        return list(zip(xs, ys))
    m = (end.y - start.y) / (end.x - start.x)
    f = lambda x: (m * (x - start.x)) + start.y
    for x in range(start.x, end.x, step):
        points.append((x, f(x)))

    return points


def line_length(start, end):
    return math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
