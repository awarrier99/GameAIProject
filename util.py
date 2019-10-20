import math
import queue


class Actions:
    U = 'Up'
    UR = 'Up Right'
    R = 'Right'
    DR = 'Down Right'
    D = 'Down'
    DL = 'Down Left'
    L = 'Left'
    UL = 'Up Left'


class Loc:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        if not other or type(other) is not Loc:
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return (53 + hash(self.x)) * 53 + hash(self.y)


class Node:
    def __init__(self, x, y):
        self.loc = Loc(x, y)

    def __str__(self):
        return 'Node: {}'.format(str(self.loc))

    def __eq__(self, other):
        if not other or type(other) is not Node:
            return False
        return self.loc == other.loc

    def __hash__(self):
        return hash(self.loc)


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

# def createNode(state, metadata=None):
#     if not metadata:
#         metadata = {'path_key': None, 'action': None, 'cost': None}
#     return {'state': state, 'metadata': metadata}
#
# def createMetadata(current, successor, path_map, last_key):
#     path_key = current['metadata']['path_key']
#     if successor:
#         metadata = successor['metadata']
#         path_map[last_key] = (path_key, metadata['action'])
#         metadata['path_key'] = last_key
#         metadata['cost'] += current['metadata']['cost']
#
# def pathfind(start, end):
#     nodes = queue.PriorityQueue()
#     visited = set()
#
#     current = start
#
#     while current is not end:
#         parent = current.loc
#         if parent not in visited:
#             visited.add(parent)
#             for successor in problem.getSuccessors(parent):
#                 if successor not in visited:
#                     successor = createNode(successor[0],
#                                            metadata={'action': successor[1], 'cost': successor[2]})
#                     last_key += 1
#                     createMetadata(current, successor, path_map, last_key)
#                     if alg_type == 'UCS':
#                         nodes.push(successor, successor['metadata']['cost'])
#                     else:
#                         nodes.push(successor)
#
#         current = nodes.pop()
#
#     path = []
#     prev_key = current['metadata']['path_key']
#
#     # states = []
#
#     while path_map[prev_key][0] is not None:
#         path.insert(0, path_map[prev_key][1])
#
#         # states.insert(0, path_map[prev_key][2])
#
#         prev_key = path_map[prev_key][0]
#
#     # for i, _ in enumerate(path):
#     #     est = heuristic(states[i], problem)
#     #     act = len(path) - i
#     #     # if est > act:
#     #     print 'est:', est, 'act:', act
#
#     return path
#
# def get_waypoint(self):
#         # get the next wayPoint
#
# def get_heuristic(self, state, goalState):
#     sx ,sy = state
#     ex, ey = goalState
#
#     dx = sx - ex
#     dy = sy - ey
#
#     return math.sqrt(dx ** 2 + dy ** 2)






