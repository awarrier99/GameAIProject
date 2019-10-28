from Workers import Workers
from util import pathfind, euclidean_heuristic


class AI:
    def __init__(self, neighbors, cb, ecb, heuristic=euclidean_heuristic):
        self._resolved = True
        self.neighbors = neighbors
        self.heuristic = heuristic
        self.wcb = cb
        self.ecb = ecb
        self._last_locs = (None, None)

    def cb(self, result):
        self._resolved = True
        self.wcb(result)

    def pathfind(self, start, end):
        if self._resolved and (not self._last_locs == (start, end)):
            self._resolved = False
            self._last_locs = (start, end)
            Workers.delegate(pathfind, (self.neighbors, start, end, self.heuristic), callback=self.cb,
                             error_callback=self.ecb)
