from multiprocessing import Pool
from util import pathfind, euclidean_heuristic


class AI:
    def __init__(self, grid, cb, ecb, heuristic=euclidean_heuristic):
        self._pool = Pool(1)
        self._resolved = True
        self.grid = grid
        self.heuristic = heuristic
        self.wcb = cb
        self.ecb = ecb

    def cb(self, result):
        self._resolved = True
        self.wcb(result)

    def pathfind(self, start, end):
        if self._resolved:
            self._resolved = False
            self._pool.apply_async(pathfind, (self.grid, start, end, self.heuristic), callback=self.cb, error_callback=self.ecb)
