# -*- coding: utf-8 -*-

import random
from transition_model import get_next_state
from game_map_objects import GameMapObjects


class Learner(object):

    def __init__(self, alpha=0.0002, gamma=0.07):
        self.weights = [0] * 25
        self.weights[12] = 1

        self.alpha = alpha
        self.gamma = gamma

    def _get_utility(self, state):
        state_rewards = self._get_state_rewards(state)
        return sum(w * r for w, r in zip(self.weights, state_rewards))

    def get_optimal_action(self, game):
        optimal_utility = float("-inf")
        optimal_actions = [0]  # noop.

        for a in game.available_actions():
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
            self.weights[i] += (
                self.alpha *
                (real_utility - guess_utility) * state_rewards[i])

    def _get_state_rewards(self, state):
        height, width = state.shape
        state_rewards = []

        for i in range(height):
            for j in range(width):
                state_rewards.append(GameMapObjects.to_reward(state[i, j]))

        return state_rewards
