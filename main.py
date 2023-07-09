import numpy as np
import matplotlib.pyplot as plt
from agent import Agent
from Env import Environment


class My_class:
  def my_sym(self, sym):
    self.sym = sym

  def action(self, env):
    while True:
      move = input("Введите координаты для хода через пробел (0-2): ")
      i, j = move.split(' ')
      i = int(i)
      j = int(j)
      if env.is_empty(i, j):
        env.board[i,j] = self.sym
        break

  def update(self, env):
    pass

  def update_history(self, s):
    pass


def get_state_winner(env, i=0, j=0):
  results = []

  for v in (0, env.agent1, env.agent2):
    env.board[i,j] = v
    if j == 2:
      if i == 2:
        state = env.get_state()
        ended = env.game_over(rec=True)
        winner = env.winner
        results.append((state, winner, ended))
      else:
        results += get_state_winner(env, i + 1, 0)
    else:
      results += get_state_winner(env, i, j + 1)

  return results


def initial_cost_x(env, state_winner_triples):
  c = np.zeros(env.num_states)
  for state, winner, ended in state_winner_triples:
    if ended:
      if winner == env.agent1:
        v = 1
      else:
        v = 0
    else:
      v = 0.5
    c[state] = v
  return c


def initial_cost_o(env, state_winner_triples):
  c = np.zeros(env.num_states)
  for state, winner, ended in state_winner_triples:
    if ended:
      if winner == env.agent2:
        v = 1
      else:
        v = 0
    else:
      v = 0.5
    c[state] = v
  return c


def play_game(agent1, agent2, env, draw=False):
  current_player = None
  while not env.game_over():
    if current_player == agent1:
      current_player = agent2
    else:
      current_player = agent1

    if draw:
      if draw == 1 and current_player == agent1:
        env.draw_board()
      if draw == 2 and current_player == agent2:
        env.draw_board()

    current_player.action(env)

    state = env.get_state()
    agent1.update_history(state)
    agent2.update_history(state)

  if draw:
    env.draw_board()

  agent1.update(env)
  agent2.update(env)


if __name__ == '__main__':
  agent1 = Agent()
  agent2 = Agent()

  env = Environment()
  state_winner_triples = get_state_winner(env)


  cx = initial_cost_x(env, state_winner_triples)
  agent1.cost_func(cx)
  co = initial_cost_o(env, state_winner_triples)
  agent2.cost_func(co)

  agent1.agent_X_O(env.agent1)
  agent2.agent_X_O(env.agent2)

  T = 10000
  for t in range(T):
    if t % 200 == 0:
      print(t)
    play_game(agent1, agent2, Environment())

  iam = My_class()
  iam.my_sym(env.agent2)
  while True:
    agent2.show_cost(True)
    play_game(agent1, iam, Environment(), draw=2)
    answer = input("Еще раз? [Y/n]: ")
    if answer and answer.lower()[0] == 'n':
      break