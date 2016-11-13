# -*- coding: utf-8 -*-

import sys
import random
from game_map import GameMap, SlicedGameMap
from game_map_objects import GameMapObjects
from ale_python_interface import ALEInterface


class MsPacManGame(object):

    """Ms. Pac-Man Arcade Learning Environment wrapper class."""

    def __init__(self, seed, display):
        """Constructs a MsPacManGame.

        Args:
            seed: Initial random seed, randomized when None.
            display: Whether to display onto the screen or not.
        """
        self._ale = ALEInterface()

        if seed is None:
            seed = random.randint(0, 25500)
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

        self._lives = self._ale.lives()

        self._update_state()

        self._go_to((94, 98), 3)

    @property
    def lives(self):
        """Current lives remaining."""
        return self._lives

    @property
    def reward(self):
        """Current total reward."""
        return self._reward

    @property
    def map(self):
        """Current game map."""
        return self._map

    @property
    def sliced_map(self):
        """Current game slice map."""
        return self._sliced_map

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
        actions = []

        for action, move in [
            (2, (-1, 0)),  # up
            (3, (0, 1)),   # right
            (4, (0, -1)),  # left
            (5, (1, 0))    # down
        ]:
            new_pos = self.get_next_position(move)
            if 0 <= new_pos[0] < GameMap.HEIGHT:
                if self._map.map[new_pos] != GameMapObjects.WALL:
                    actions.append(action)
        return actions

    def action_to_move(self, action):
        return [(-1, 0), (0, 1), (0, -1), (1, 0)][action - 2]

    def get_next_position(self, move):
        new_pos = (
            self.ms_pacman_position[0] + move[0],
            self.ms_pacman_position[1] + move[1]
        )
        if new_pos[1] < 0:
            new_pos = (new_pos[0], new_pos[1] + GameMap.WIDTH)
        elif new_pos[1] >= GameMap.WIDTH:
            new_pos = (new_pos[0], new_pos[1] - GameMap.WIDTH)
        return new_pos

    def act(self, action):
        """Plays a given action in the game.

        Args:
            action: Action to play.

        Returns:
            Partial reward gained since last action.
        """
        m = self.action_to_move(action)
        next_pos = self.get_next_position(m)
        old_reward = self._reward
        old_lives = self._lives
        old_pos = self._ms_pacman_position

        expected_reward = GameMapObjects.to_reward(self._map.map[next_pos])

        if expected_reward <= 0:
            while self._ms_pacman_position != next_pos:
                if self._ms_pacman_position != old_pos:
                    break
                if self.game_over() or self._lives < old_lives:
                    return GameMapObjects.to_reward(GameMapObjects.GHOST)
                self._reward += self._ale.act(action)
                self._update_state()

        else:
            while self._reward == old_reward:
                if self._ms_pacman_position not in (old_pos, next_pos):
                    break
                if self.game_over() or self._lives < old_lives:
                    return GameMapObjects.to_reward(GameMapObjects.GHOST)
                self._reward += self._ale.act(action)
                self._update_state()

        self._update_map()
        return self._reward - old_reward

    def _go_to(self, raw_pos, action):
        while abs(self._raw_ms_pacman_position[0] - raw_pos[0]) > 1 or \
                abs(self._raw_ms_pacman_position[1] - raw_pos[1]) > 1:
            self._ale.act(action)
            self._update_state()
        self._update_map()

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
        i = round((y - 2) / 12.0)
        if x < 83:
            j = round((x - 18) / 8.0 + 1)
        elif 93 < x < 169:
            j = round((x - 22) / 8.0 + 1)
        elif x > 169:
            j = 0
        elif x < 88:
            j = 9
        else:
            j = 10
        return i, j

    def _to_raw_position(self, pos):
        i, j = pos
        y = i * 12 + 2
        if j == 0:
            x = 12
        elif j <= 9:
            x = (j - 1) * 8 + 18
        else:
            x = (j - 1) * 8 + 22
        return x, y

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

        # Update lives.
        self._lives = self._ale.lives()

    def _update_map(self):
        # Get new map from screen.
        self._ale.getScreen(self.__screen)
        self._map = GameMap(self.__screen.reshape(210, 160))
        self._map.map[self._ms_pacman_position] = GameMapObjects.MS_PACMAN
        for ghost_pos in self._ghost_positions:
            self._map.map[ghost_pos] = GameMapObjects.GHOST
        self._sliced_map = SlicedGameMap(self._map,
                                         self._ms_pacman_position)
