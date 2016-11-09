#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from random import randrange
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
    actions = game.available_actions()

    for episode in range(args.episodes):
        total_reward = 0
        while not game.game_over():
            a = actions[randrange(len(actions))]
            total_reward += game.act(a)
        print("episode {}: {}".format(episode + 1, total_reward))
        game.reset_game()
