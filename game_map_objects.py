# -*- coding: utf-8 -*-


class GameMapObjects(object):

    """Game map object enumerations."""

    EMPTY = 0
    WALL = 1
    PELLET = 2
    POWER_UP = 3
    GHOST = 4
    MS_PACMAN = 5

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
        elif classification == GameMapObjects.GHOST:
            color = [0, 0, 255]  # Red
        elif classification == GameMapObjects.MS_PACMAN:
            color = [0, 255, 0]  # Green.
        return color
