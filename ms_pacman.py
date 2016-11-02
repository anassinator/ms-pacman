#!/usr/bin/env python

import sys
import argparse
from random import randrange
from ale_python_interface import ALEInterface


def get_interface(args):
    """Gets Arcade Learning Environment Interface.

    Args:
        args: Command-line arguments.

    Returns:
        ALEInterface.
    """
    ale = ALEInterface()

    if args.seed:
        ale.setInt("random_seed", args.seed)

    if args.display:
        if sys.platform == "darwin":
            # Use PyGame in macOS.
            import pygame
            pygame.init()

            # Sound doesn't work on macOS.
            ale.setBool("sound", False)
        elif sys.platform.startswith("linux"):
            ale.setBool("sound", True)

        ale.setBool("display_screen", True)

    ale.loadROM("MS_PACMAN.BIN")

    return ale


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
    ale = get_interface(args)
    actions = [
        0,  # noop
        1,  # fire
        2,  # up
        3,  # right
        4,  # left
        5   # down
    ]

    for episode in range(args.episodes):
        total_reward = 0
        while not ale.game_over():
            a = actions[randrange(len(actions))]
            total_reward += ale.act(a)
        print("episode {}: {}".format(episode + 1, total_reward))
        ale.reset_game()
