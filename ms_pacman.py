# -*- coding: utf-8 -*-

import sys
from game_map import GameMap, GameMapObjects
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
        self._ms_pacman_direction = self._raw_ms_pacman_position = (0, 0)
        self._ghost_directions = self._raw_ghost_positions = [(0, 0)] * 4

        self.__screen = self._ale.getScreen()
        self.__ram = self._ale.getRAM()

        self._update_state()

    @property
    def reward(self):
        """Current total reward."""
        return self._reward

    @property
    def map(self):
        """Current game map."""
        return self._map

    @property
    def ms_pacman_position(self):
        """Ms. PacMan's position as a map index."""
        return self._ms_pacman_position

    @property
    def ghost_positions(self):
        """Ghost positions as a list of map indices."""
        return self._ghost_positions

    @property
    def ms_pacman_direction(self):
        """Ms. PacMan's direction as an (x, y) tuple."""
        return self._ms_pacman_direction

    @property
    def ghost_directions(self):
        """Ghost directions as a list of (x, y) tuples."""
        return self._ghost_directions

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

    def _get_direction(self, prev, curr, prev_direction):
        """Computes the relative direction from one position to another.

        Args:
            prev: Previous (x, y) position.
            curr: Current (x, y) position.
            prev_direction: Previous direction.

        Returns:
            Relative direction.
        """
        new_direction = (curr[0] - prev[0], curr[1] - prev[1])
        return new_direction if new_direction != (0, 0) else prev_direction

    def _to_map_position(self, pos):
        """Converts a RAM coordinate into a map coordinate.

        Args:
            pos: (x, y) coordinates from RAM.

        Returns:
            Map index coordinate.
        """
        x, y = pos
        i = round((y - 2) / 12)
        if x < 83:
            j = round((x - 18) / 8 + 1)
        elif 93 < x < 169:
            j = round((x - 22) / 8 + 1)
        elif x > 169:
            j = 0
        elif x < 88:
            j = 9
        else:
            j = 10
        return (i, j)

    def _update_state(self):
        """Updates the internal state of the game."""
        # Get new states from RAM.
        self._ale.getRAM(self.__ram)
        new_ms_pacman_position = (int(self.__ram[10]), int(self.__ram[16]))
        new_ghost_positions = [
            (int(self.__ram[6]), int(self.__ram[12])),
            (int(self.__ram[7]), int(self.__ram[13])),
            (int(self.__ram[8]), int(self.__ram[14])),
            (int(self.__ram[9]), int(self.__ram[15]))
        ]

        # Update directions.
        self._ms_pacman_direction = self._get_direction(
            self._raw_ms_pacman_position, new_ms_pacman_position,
            self._ms_pacman_direction)
        self._ghost_directions = [
            self._get_direction(self._raw_ghost_positions[i],
                                new_ghost_positions[i],
                                self._ghost_directions[i])
            for i in range(len(new_ghost_positions))
        ]

        # Update positions.
        self._raw_ms_pacman_position = new_ms_pacman_position
        self._raw_ghost_positions = new_ghost_positions
        self._ms_pacman_position = self._to_map_position(
            new_ms_pacman_position)
        self._ghost_positions = map(self._to_map_position, new_ghost_positions)

        # Get new map from screen.
        if self._ale.getFrameNumber() % 10 == 0:
            self._ale.getScreen(self.__screen)
            self._map = GameMap(self.__screen.reshape(210, 160))
            self._map.map[self._ms_pacman_position] = GameMapObjects.MS_PACMAN
            for ghost_pos in self._ghost_positions:
                self._map.map[ghost_pos] = GameMapObjects.GHOST
