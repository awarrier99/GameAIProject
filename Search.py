import math

class Search:

    def __init__(self, world):
        self.world = world

    def find_path(self, startNode, endNode):

        openList = PriorityQueue()  # UCS and A*

        visitedList = set()  # initialize closed list as empty list
        current = startNode, None, 0, []  # node has position and action

        while not problem.isGoalState(current[0]):  # loop while the current state is not the goal state
            if not current[0] in visitedList:  # if the current parent node is not visited
                visitedList.add(current[0])  # add the current state to the visited list

                for child in problem.getSuccessors(current[0]):  # loop through the children of the current node
                    if child[0] not in visitedList:
                        cost = child[2] + current[2]
                        actions = current[3] + [child[1]]

                        openList.push(child, child[2] + heuristic(child[0], problem))

            current = openList.pop()  # set the current node to the next open node in the stack

        return current[3]

    def get_waypoint(self):
            # get the next wayPoint

    def get_heuristic(self, state, goalState):
        sx ,sy = state
        ex, ey = goalState

        dx = sx - ex
        dy = sy - ey

        return math.sqrt(dx ** 2 + dy ** 2)






