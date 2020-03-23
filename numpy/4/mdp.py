from utils import trans_id
from abc import ABC, abstractmethod
import time
import numpy as np
import line_profiler


class MDP(ABC):
    """Base environment for the dynamic programming chapter."""

    def __init__(self):
        self.init_p()

    def renormalize(self):
        for s in self.states:
            for a in self.moves:
                p_sum = sum([self.p[(s_p, r, s, a)] for s_p in self.states
                             for r in self.r])
                if p_sum > 0:
                    for s_p in self.states:
                        for r in self.r:
                            self.p[(s_p, r, s, a)] /= p_sum

    def init_p(self):
        print("starting to compute transitions p...")
        start = time.time()
        self.p = {(s_p, r, s, a): self._p(s_p, r, s, a)
                  for s in self.states for a in self.moves
                  for s_p in self.states for r in self.r}
        # hardcoded normalization to avoid overflow
        self.renormalize()

        def p_sum(s_p_list, r_list, s_list, a_list):
            return np.sum([self.p[(s_p, r, s, a)] for s_p in s_p_list
                           for r in r_list for s in s_list for a in a_list])
        self.pr = {(s, a): np.array([p_sum(self.states, [r], [s], [a]) for r in self.r])
                   for s in self.states for a in self.moves}
        self.psp = {(s, a): np.array([p_sum([s_p], self.r, [s], [a])
                             for s_p in self.states])
                    for s in self.states for a in self.moves}
        # def normalize(d): return {(s, a): (1 / sum(d[s, a])) * d[s, a]
        #                           for s in self.states for a in self.moves}
        # self.pr = normalize(self.pr)
        # print(self.psp[(0,0), 0])
        # input("after->")
        # self.psp = normalize(self.psp)
        # print(self.psp[(0,0), 0])
        # input()
        # import ipdb; ipdb.set_trace()
        print(f"finished after {time.time()-start}s")

    @abstractmethod
    def _p(self, s_p, r, s, a):
        """Specific transition probabilities for environment."""
        raise NotImplementedError

    @property
    @abstractmethod
    def states(self):
        """List of possible states."""
        raise NotImplementedError

    @property
    @abstractmethod
    def r(self):
        """List of possible rewards."""
        raise NotImplementedError

    @property
    @abstractmethod
    def moves(self):
        """List of all available actions."""
        raise NotImplementedError
