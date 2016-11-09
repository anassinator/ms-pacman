# -*- coding: utf-8 -*-

import sys
from ale_python_interface import ALEInterface


class MsPacManGame(object):

    """Ms. Pac-Man Arcade Learning Environment wrapper class."""

    def __init__(self, seed, display):
        """Constructs a MsPacManGame.

        Args:
            seed: Initial random seed.
            display: Whether to display onto the screen or not.
        """
        self._ale = ALEInterface()

        if seed:
            self._ale.setInt("random_seed", seed)

        if display:
            if sys.platform == "darwin":
                # Use PyGame in macOS.
                import pygame
                pygame.init()

                # Sound doesn't work on macOS.
                self._ale.setBool("sound", False)
            elif sys.platform.startswith("linux"):
                self._ale.setBool("sound", True)

            self._ale.setBool("display_screen", True)

        self._ale.loadROM("MS_PACMAN.BIN")

        self._reward = 0

        self.__ram = self._ale.getRAM()
        self._update_state()

    @property
    def reward(self):
        """Current total reward."""
        return self._reward

    @property
    def ms_pacman_position(self):
        """Ms. PacMan's position as an (x, y) tuple."""
        return self._ms_pacman_position

    @property
    def ghost_positions(self):
        """Ghost positions as a list of (x, y) tuples."""
        return self._ghost_positions

    def available_actions(self):
        """Returns a list of available actions to consider."""
        return [
            0,  # noop
            1,  # fire
            2,  # up
            3,  # right
            4,  # left
            5   # down
        ]

    def act(self, action):
        """Plays a given action in the game.

        Args:
            action: Action to play.

        Returns:
            Partial reward gained since last action.
        """
        self._update_state()
        partial_reward = self._ale.act(action)
        self._reward += partial_reward
        return partial_reward

    def game_over(self):
        """Returns whether the game reached a terminal state or not."""
        return self._ale.game_over()

    def reset_game(self):
        """Resets the game to the initial state."""
        self._reward = 0
        return self._ale.reset_game()

    def _update_state(self):
        """Updates the internal state of the game."""
        self._ale.getRAM(self.__ram)
        self._ms_pacman_position = (self.__ram[10], self.__ram[16])
        self._ghost_positions = [
            (self.__ram[6], self.__ram[12]),
            (self.__ram[7], self.__ram[13]),
            (self.__ram[8], self.__ram[14]),
            (self.__ram[9], self.__ram[15])
        ]
