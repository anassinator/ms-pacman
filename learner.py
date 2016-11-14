# -*- coding: utf-8 -*-

import os
import pickle
import random
from transition_model import get_next_state
from game_map_objects import GameMapObjects


class Learner(object):

    WEIGHTS_FILE = "weights.p"

    def __init__(self, alpha=0.000001, gamma=0.7):
        if not os.path.isfile(self.WEIGHTS_FILE):
            self.weights = [
                0.06, 0.12, 0.25, 0.12, 0.06,
                0.12, 0.25, 0.50, 0.25, 0.12,
                0.25, 0.50, 1.00, 0.50, 0.25,
                0.12, 0.25, 0.50, 0.25, 0.12,
                0.06, 0.12, 0.25, 0.12, 0.06
            ]
        else:
            self.weights = pickle.load(open(self.WEIGHTS_FILE, "rb"))

        self.alpha = alpha
        self.gamma = gamma

    def _get_utility(self, state):
        state_rewards = self._get_state_rewards(state)
        return sum(w * r for w, r in zip(self.weights, state_rewards))

    def get_optimal_action(self, game):
        optimal_utility = float("-inf")
        optimal_actions = [0]  # noop.
        available_actions = game.available_actions()

        ghost_in_view = any(x == GameMapObjects.BAD_GHOST
                            for x in game.sliced_map.map.flatten())

        # Explore.
        if not ghost_in_view and random.random() < 0.10:
            a = random.choice(available_actions)
            utility = self._get_utility(get_next_state(game, a))
            return a, utility

        for a in available_actions:
            next_state = get_next_state(game, a)
            utility = self._get_utility(next_state)
            if utility > optimal_utility:
                optimal_utility = utility
                optimal_actions = [a]
            elif utility == optimal_utility:
                optimal_actions.append(a)

        return (random.choice(optimal_actions), optimal_utility)

    def update_weights(self, prev_state, game, guess_utility, reward):
        state_rewards = self._get_state_rewards(prev_state)
        real_utility = reward + self.gamma * self.get_optimal_action(game)[1]
        print(guess_utility, real_utility)

        for i in range(25):
            self.weights[i] = \
                (1 - self.alpha) * self.weights[i] + \
                self.alpha * (real_utility - guess_utility) * state_rewards[i]

    def _get_state_rewards(self, state):
        height, width = state.shape
        state_rewards = []

        for i in range(height):
            for j in range(width):
                state_rewards.append(GameMapObjects.to_reward(state[i, j]))

        return state_rewards

    def human_readable_weights(self):
        s = ""
        for i in range(25):
            s += "{:+3.2f} ".format(self.weights[i])
            if i % 5 == 4:
                s += "\n"
        return s

    def save(self):
        pickle.dump(self.weights, open(self.WEIGHTS_FILE, "wb"))
