import numpy as np


class Agent:
  def __init__(self, e=0.1, lr=0.5):
    self.e = e 
    self.lr = lr 
    self.flag = False
    self.history = []
  
  def cost_func(self, c):
    self.c = c

  def agent_X_O(self, sym):
    self.agent_sym = sym

  def show_cost(self, cost):
    self.sh = cost

  def del_history(self):
    self.history = []

  def action(self, env):
    r = np.random.rand()
    best_state = None
    if r < self.e:
      possible_moves = []
      for i in range(3):
        for j in range(3):
          if env.is_empty(i, j):
            possible_moves.append((i, j))
      random_move = np.random.choice(len(possible_moves))
      next_move = possible_moves[random_move]
    else:
      pos2value = {}
      next_move = None
      best_value = -1
      for i in range(3):
        for j in range(3):
          if env.is_empty(i, j):
            env.board[i,j] = self.agent_sym
            state = env.get_state()
            env.board[i,j] = 0
            pos2value[(i,j)] = self.c[state]
            if self.c[state] > best_value:
              best_value = self.c[state]
              best_state = state
              next_move = (i, j)

      if self.flag:
        for i in range(3):
          print("------------------")
          for j in range(3):
            if env.is_empty(i, j):
              print(" %.2f|" % pos2value[(i,j)], end="")
            else:
              print("  ", end="")
              if env.board[i,j] == env.agent1:
                print("x  |", end="")
              elif env.board[i,j] == env.agent2:
                print("o  |", end="")
              else:
                print("   |", end="")
          print("")
        print("------------------")

    env.board[next_move[0], next_move[1]] = self.agent_sym

  def update_history(self, s):
    self.history.append(s)

  def update(self, env):
    reward = env.reward(self.agent_sym)
    target = reward
    for h in reversed(self.history):
      value = self.c[h] + self.lr*(target - self.c[h])
      self.c[h] = value
      target = value
    self.del_history()