#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import argparse
from random import randrange
from ms_pacman import MsPacManGame
from learner import Learner
from transition_model import *


def get_args():
    """Gets parsed command-line arguments.

    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="plays Ms. Pac-Man")
    parser.add_argument("--episodes", default=10, type=int,
                        help="number of episodes to run")
    parser.add_argument("--display", action="store_true", default=False,
                        help="whether to display the game on screen or not")
    parser.add_argument("--seed", default=None, type=int,
                        help="seed for random number generator to use")

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    game = MsPacManGame(args.seed, args.display)
    learning_agent = Learner()

    for episode in range(args.episodes):
        old_reward = 0
        while not game.game_over():
            print(learning_agent.weights)
            actions = game.available_actions()
            optimal_a = 0
            optimal_utility = float("-Infinity")
            for a in actions:
                next_state = get_next_state(game, a)
                utility = learning_agent.get_utility(next_state)
                if utility > optimal_utility:
                    optimal_utility = utility
                    optimal_a = a
            # next_pos = get_next_position(game, optimal_a)
            # while game.ms_pacman_position != next_pos and \
            #         old_reward == game.reward:
            #     print(game.reward)
            #     game.act(optimal_a)
            game.act(optimal_a)
            real_utility = game.reward - old_reward
            old_reward = game.reward
            learning_agent.update_weights(
                game.sliced_map.map,
                optimal_utility,
                real_utility
            )
            game_map = game.map
            sliced_game_map = game.sliced_map

            if args.display:
                cv2.imshow("map", game_map.to_image())
                cv2.imshow("sliced map", sliced_game_map.to_image())
                cv2.waitKey(1)
        print("episode {}: {}".format(episode + 1, game.reward))
        game.reset_game()
