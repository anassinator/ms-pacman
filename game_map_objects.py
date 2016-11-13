# -*- coding: utf-8 -*-


class Ghost(object):

    """Ghost."""

    BAD = 0
    GOOD = 1

    def __init__(self, pos, state, direction):
        self.pos = pos
        self.state = state
        self.direction = direction

    @classmethod
    def from_ram(self, pos, ram):
        direction_ram = ram & 3
        direction = \
            [-1, 0] if direction_ram == 0 else \
            [0, 1] if direction_ram == 1 else \
            [1, 0] if direction_ram == 2 else \
            [0, -1]

        edible_ram = (ram >> 7) & 1
        state = \
            Ghost.GOOD if edible_ram == 1 else \
            Ghost.BAD

        return Ghost(pos, state, direction)


class GameMapObjects(object):

    """Game map object enumerations."""

    EMPTY = 0
    WALL = 1
    PELLET = 2
    POWER_UP = 3
    GOOD_GHOST = 4
    BAD_GHOST = 5
    FRUIT = 6
    MS_PACMAN = 7

    @classmethod
    def to_reward(cls, classification):
        """Converts a GameMapObject to a reward.

        Args:
            classification: GameMapObject.

        Returns:
            Reward.
        """
        reward = 0
        if classification == GameMapObjects.WALL:
            reward = 0
        elif classification == GameMapObjects.PELLET:
            reward = 10
        elif classification == GameMapObjects.POWER_UP:
            reward = 50
        elif classification == GameMapObjects.GOOD_GHOST:
            reward = 200
        elif classification == GameMapObjects.BAD_GHOST:
            reward = -100
        elif classification == GameMapObjects.FRUIT:
            reward = 100
        elif classification == GameMapObjects.MS_PACMAN:
            reward = 0
        return reward

    @classmethod
    def to_color(cls, classification):
        """Converts a GameMapObject to an BGR color.

        Args:
            classification: GameMapObject.

        Returns:
            BGR color.
        """
        color = [136, 28, 0]  # Dark blue.
        if classification == GameMapObjects.WALL:
            color = [111, 111, 228]  # Pink-ish.
        elif classification == GameMapObjects.PELLET:
            color = [255, 255, 255]  # White.
        elif classification == GameMapObjects.POWER_UP:
            color = [255, 255, 0]  # Cyan.
        elif classification == GameMapObjects.GOOD_GHOST:
            color = [0, 255, 0]  # Green.
        elif classification == GameMapObjects.BAD_GHOST:
            color = [0, 0, 255]  # Red.
        elif classification == GameMapObjects.FRUIT:
            color = [255, 0, 255]  # Magenta.
        elif classification == GameMapObjects.MS_PACMAN:
            color = [0, 255, 255]  # Yellow.
        return color
