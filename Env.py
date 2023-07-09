import numpy as np


class Environment:
  def __init__(self):
    self.board = np.zeros((3, 3))
    self.agent1 = -1
    self.agent2 = 1
    self.winner = None
    self.ended = False
    self.num_states = 3**(3*3)

  def is_empty(self, i, j):
    return self.board[i,j] == 0

  def reward(self, sym):
    if not self.game_over():
      return 0

    return 1 if self.winner == sym else 0

  def get_state(self):
    k = 0
    h = 0
    for i in range(3):
      for j in range(3):
        if self.board[i,j] == 0:
          v = 0
        elif self.board[i,j] == self.agent1:
          v = 1
        elif self.board[i,j] == self.agent2:
          v = 2
        h += (3**k) * v
        k += 1
    return h

  def game_over(self, rec=False):
    if not rec and self.ended:
      return self.ended
    
    for i in range(3):
      for player in (self.agent1, self.agent2):
        if self.board[i].sum() == player*3:
          self.winner = player
          self.ended = True
          return True

    for j in range(3):
      for player in (self.agent1, self.agent2):
        if self.board[:,j].sum() == player*3:
          self.winner = player
          self.ended = True
          return True

    for player in (self.agent1, self.agent2):
      if self.board.trace() == player*3:
        self.winner = player
        self.ended = True
        return True
      if np.fliplr(self.board).trace() == player*3:
        self.winner = player
        self.ended = True
        return True

    if np.all((self.board == 0) == False):
      self.winner = None
      self.ended = True
      return True

    self.winner = None
    return False

  def is_draw(self):
    return self.ended and self.winner is None

  def draw_board(self):
    for i in range(3):
      print("-------------")
      for j in range(3):
        print("  ", end="")
        if self.board[i,j] == self.agent1:
          print("x ", end="")
        elif self.board[i,j] == self.agent2:
          print("o ", end="")
        else:
          print("  ", end="")
      print("")
    print("-------------")