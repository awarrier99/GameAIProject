from util import Node, Wall, Loc, directions, actions


class Grid:
    def __init__(self, x, y, walls=[]):
        self.size = self.width, self.height = x, y
        self._grid = [['N' for _ in range(self.height)] for _ in range(self.width)]
        self.walls = walls
        for wall in self.walls:
            self._grid[wall.x][wall.y] = 'W'
        self.__first = None

    def neighbors(self, node):
        if not node:
            return []

        node_list = []

        for idx, dr in enumerate(directions):
            loc = Loc(node.loc.x + dr[0], node.loc.y + dr[1])
            if self.is_valid(loc):
                n = self[loc.x][loc.y]
                if not n.is_wall():
                    n.action = actions[idx]
                    if dr[0] and dr[1]:
                        n.cost = 2 ** 0.5
                    else:
                        n.cost = 1
                    node_list.append(n)

        return node_list

    def is_blocked(self, node, direction):
        if direction[0] == 0 or direction[1] == 0:
            return False
        adjacent1 = self[node.loc.x + direction[0]][node.loc.y]
        adjacent2 = self[node.loc.x][node.loc.y + direction[1]]
        return adjacent1.is_wall() and adjacent2.is_wall()

    def is_valid(self, loc):
        if loc.x < 0 or loc.y < 0:
            return False
        if loc.x >= self.width:
            return False
        if loc.y >= self.height:
            return False

        return True

    def __getitem__(self, idx):
        return GridCol(idx, self)

    def __str__(self):
        string = ''
        for i in range(self.height):
            for j in range(self.width):
                string += self._grid[j][i] + '  '

            string = string[:-2]
            string += '\n'

        return string


class GridCol:
    def __init__(self, col_num, grid):
        self._col_num = col_num
        self.grid = grid

    def __getitem__(self, idx):
        if not self.grid.is_valid(Loc(self._col_num, idx)):
            return Wall(Loc(-1, -1))

        if self.grid._grid[self._col_num][idx] == 'W':
            return Wall(Loc(self._col_num, idx))

        return Node(Loc(self._col_num, idx))

    def __setitem__(self, idx, value):
        self.grid._grid[self._col_num][idx] = value
