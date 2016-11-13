# -*- coding: utf-8 -*-

from game_map_objects import GameMapObjects


class Learner(object):
    def __init__(self, alpha=0.2):
        self.weights = [0] * 25
        self.weights[12] = 1
        self.alpha = alpha

    def get_utility(self, state):
        state_rewards = self.get_state_rewards(state)
        print(state)
        print(state_rewards)
        print(self.weights)
        return sum(w * r for w, r in zip(self.weights, state_rewards))

    def update_weights(self, state, guess_utility, real_utility):
        state_rewards = self.get_state_rewards(state)
        print(guess_utility, real_utility)

        for i in range(25):
            self.weights[i] += self.alpha * (real_utility - guess_utility) * \
                state_rewards[i]

    def get_state_rewards(self, state):
        height, width = state.shape
        state_rewards = []

        for i in range(height):
            for j in range(width):
                state_rewards.append(GameMapObjects.to_reward(state[i, j]))

        return state_rewards
