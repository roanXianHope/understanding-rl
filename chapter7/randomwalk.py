import numpy as np

N_STATES = 19
EMPTY_MOVE = 0
P_LEFT = 0.5
R_STEP = 0
ABSORBING_STATE = N_STATES
LEFT = 0
RIGHT = 1

class RandomWalk:
  def __init__(self, n_states=None):
    self.n_states = N_STATES if n_states is None else n_states
    self.absorbing_state = self.n_states
    self.get_states()
    self.get_moves()
    self.get_moves_d()
    self.reset()
    print(self.n_states)

  def get_moves(self):
    self.moves = [EMPTY_MOVE]

  def get_moves_d(self):
    self.moves_d = {s: self.moves for s in self.states}

  def get_states(self):
    self.states = list(range(self.n_states)) + [self.absorbing_state]

  def sample_shift(self):
    return np.sign(np.random.random() - P_LEFT)

  def step(self, action):
    shift = self.sample_shift()
    #print(f"shift={shift}")
    new_state = self.state + shift
    if not (0 <= new_state < self.n_states):
      r = -1 + 2 * (new_state == self.n_states)
      return ABSORBING_STATE, r, True, {}
    self.state = new_state
    return self.state, R_STEP, False, {}

  def reset(self):
    self.state = self.n_states // 2
    return self.state

  def seed(self, seed):
    np.random.seed(seed)

  def __str__(self):
    return self.state
