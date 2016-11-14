#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import argparse
from learner import Learner
from ms_pacman import MsPacManGame


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
    agent = Learner()

    for episode in range(args.episodes):
        while not game.game_over():
            print(agent.human_readable_weights())

            prev_state = game.sliced_map.map
            optimal_a, expected_utility = agent.get_optimal_action(game)
            reward = game.act(optimal_a)

            agent.update_weights(prev_state, optimal_a, game, expected_utility,
                                 reward)

            if args.display:
                game_map = game.map
                sliced_game_map = game.sliced_map

                cv2.imshow("map", game_map.to_image())
                cv2.imshow("sliced map", sliced_game_map.to_image())
                cv2.waitKey(1)

        agent.save()

        print("episode {}: {}".format(episode + 1, game.reward))
        game.reset_game()
