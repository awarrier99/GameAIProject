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
        node_list = []

        for idx, dr in enumerate(directions):
            loc = Loc(node.loc.x + dr[0], node.loc.y + dr[1])
            if self.is_valid(loc):
                n = self[loc.x][loc.y]
                if not n.is_wall():
                    n.action = actions[idx]
                    n.cost = 1
                    node_list.append(n)

        return node_list

    def is_valid(self, loc):
        if loc.x < 0 or loc.y < 0:
            return False
        if loc.x >= self.width:
            return False
        if loc.y >= self.height:
            return False

        return True

    def __getitem__(self, idx):
        return GridCol(idx, self._grid)

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
        self._grid = grid

    def __getitem__(self, idx):
        if self._grid[self._col_num][idx] == 'W':
            return Wall(Loc(self._col_num, idx))

        return Node(Loc(self._col_num, idx))

    def __setitem__(self, idx, value):
        self._grid[self._col_num][idx] = value
