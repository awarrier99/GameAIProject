from util import Node, Wall, GridLoc, directions, actions


class Grid:
    def __init__(self, x, y, walls=[]):
        self.size = self.width, self.height = x, y
        self._grid = [['N' for _ in range(self.height)] for _ in range(self.width)]
        self.walls = walls
        self._last_walls = walls.copy()
        for wall in self.walls:
            self[wall] = 'W'
        self.__first = None

    def add_wall(self, loc):
        self.walls.append(loc)
        self[loc] = 'W'

    def remove_wall(self, loc):
        self.walls.remove(loc)
        self[loc] = 'N'

    def neighbors(self, node):
        if not node:
            return []

        node_list = []

        for idx, dr in enumerate(directions):
            loc = node.loc.add(dr)
            if self.is_valid(loc):
                n = self[loc]
                if not n.is_wall():
                    n.action = actions[idx]
                    if dr.x and dr.y:
                        n.cost = 2 ** 0.5
                    else:
                        n.cost = 1
                    node_list.append(n)

        return node_list

    def is_blocked(self, node, direction):
        if not (direction.x and direction.y):
            return False
        adjacent1 = self[node.loc.add(GridLoc(direction.x, 0))]
        adjacent2 = self[node.loc.add(GridLoc(0, direction.y))]
        return adjacent1.is_wall() and adjacent2.is_wall()

    def is_valid(self, loc):
        if loc.x < 0 or loc.y < 0:
            return False
        if loc.x >= self.width:
            return False
        if loc.y >= self.height:
            return False

        return True

    def __getitem__(self, loc):
        if not self.is_valid(loc):
            return Wall(GridLoc(-1, -1))

        if self._grid[loc.x][loc.y] == 'W':
            return Wall(loc)

        return Node(loc)

    def __setitem__(self, loc, value):
        self._grid[loc.x][loc.y] = value

    def __str__(self):
        string = ''
        for i in range(self.height):
            for j in range(self.width):
                string += self._grid[j][i] + '  '

            string = string[:-2]
            string += '\n'

        return string

