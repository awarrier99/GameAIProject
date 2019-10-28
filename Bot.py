import settings

from Player import Player
from AI import AI
from traceback import print_exception
from util import Node, line_length


class Bot(Player):
    def __init__(self, location, world, move_delay=settings.move_frames):
        super().__init__(location)
        self._bot = True
        self.actions = []
        self.path = []
        self.draw_path = []
        self.collision_lines = []
        self._grid = world.grid
        self.ai = AI(world.grid.neighbors, self.ai_callback, Bot.task_error_callback)
        self.goal = self.last_goal = None
        self._recompute = False
        self.move_delay = move_delay
        self.delay_count = 0

    def handle_ai_task(self):
        recompute = (not self.goal == self.last_goal) or self._recompute
        if recompute:
            self._recompute = False
            self.end_move(flush_queue=True)

        find_path = False
        if self.goal and (not self.moving or recompute):
            find_path = True
        if find_path:
            self.ai.pathfind(Node(self.loc.to_grid()), Node(self.goal))

    def update(self):
        super().update()
        self.handle_ai_task()
        if self.delay_count > 0:
            self.delay_count -= 1

    def ai_callback(self, result):
        self.actions = []
        self.path = []
        for r in result:
            self.actions.append(r[0])
            self.path.append(r[1])
        self.draw_path = self.path.copy()
        if result:
            self.move(self.actions[0])
            for move in self.actions[1:]:
                self.moves.push(move)

    def scan_callback(self, results):
        self.collision_lines = []
        for collidable, collision_line in results:
            if line_length(collision_line[0], collision_line[len(collision_line) - 1]) < 700:
                self.collision_lines.append(collision_line)

    @staticmethod
    def task_error_callback(err):
        print('Task failed')
        print_exception(type(err), err, None)
