# -*- coding: utf-8 -*-

import os
import random
import pickle
from collections import defaultdict


class Learner(object):

    Q_FILE = "qfile.p"

    def __init__(self, gamma=0.7):
        self.gamma = gamma

        if not os.path.isfile(self.Q_FILE):
            self.Q = defaultdict(int)
        else:
            self.Q = defaultdict(int, pickle.load(open(self.Q_FILE, "rb")))

    def get_optimal_action(self, game):
        optimal_utility = float("-inf")
        optimal_actions = [0]  # noop.

        state = tuple(game.sliced_map.map.flatten())
        for a in game.available_actions():
            utility = self.Q[(state, a)]
            if utility > optimal_utility:
                optimal_utility = utility
                optimal_actions = [a]
            elif utility == optimal_utility:
                optimal_actions.append(a)

        return (random.choice(optimal_actions), optimal_utility)

    def update(self, prev_map, game, action, reward):
        prev_state = tuple(prev_map.flatten())
        utility = reward + self.gamma * self.get_optimal_action(game)[1]
        self.Q[(prev_state, action)] = utility

    def save(self):
        pickle.dump(dict(self.Q), open(self.Q_FILE, "wb"))
