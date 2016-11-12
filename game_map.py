# -*- coding: utf-8 -*-

import cv2
import numpy as np


class GameMapObjects(object):

    """Game map object enumerations."""

    EMPTY = 0
    WALL = 1
    PELLET = 2
    POWER_UP = 3
    GHOST = 4
    MS_PACMAN = 5


class GameMap(object):

    """Game map."""

    WIDTH = 20
    HEIGHT = 14

    PRIMARY_COLOR = 74
    SECONDARY_COLOR = 144
    MS_PACMAN_COLOR = 42
    GHOST_COLORS = (70, 88, 157, 217)

    def __init__(self, image):
        """Constructs a GameMap from an image.

        Args:
            image: OpenCV image.
        """
        # Discard everything but map.
        self._image = image[2:170]

        height, width = self._image.shape
        self._width_step = width / self.WIDTH
        self._height_step = height / self.HEIGHT

        self._classify()

    @property
    def map(self):
        """Map of GameMapObjects."""
        return self._map

    def _classify_histogram(self, histogram):
        """Classifies an image partition based on the dominant color.

        Args:
            histogram: Color histogram.

        Returns:
            GameMapObjects enum.
        """
        primary_count = histogram[self.PRIMARY_COLOR]
        total_count = self._width_step * self._height_step
        primary_ratio = primary_count / total_count

        # Check if wall.
        if primary_ratio >= 0.40:
            return GameMapObjects.WALL

        # Check if power up.
        if primary_ratio >= 0.25:
            return GameMapObjects.POWER_UP

        # Check if pellet.
        if primary_ratio >= 0.05:
            return GameMapObjects.PELLET

        # It's a clear path.
        return GameMapObjects.EMPTY

    def _classify_partition(self, partition):
        """Classifies a partition.

        Args:
            partition: Partition.

        Returns:
            GameMapObjects enum.
        """
        histogram = cv2.calcHist([partition], [0], None, [256], [0, 256])
        return self._classify_histogram(histogram)

    def _classify(self):
        """Classifies the entire image."""
        self._map = np.zeros((self.HEIGHT, self.WIDTH), dtype=np.uint8)
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                curr_width = i * self._width_step
                curr_height = j * self._height_step

                next_width = curr_width + self._width_step
                next_height = curr_height + self._height_step

                partition = self._image[curr_height:next_height,
                                        curr_width:next_width]

                self._map[j, i] = self._classify_partition(partition)

    def to_image(self):
        """Converts map to a viewable image.

        Returns:
            OpenCV image.
        """
        image = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                classification = self._map[j, i]
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
                image[j, i] = color

        upscaled_image = cv2.resize(image, (160, 168),
                                    interpolation=cv2.INTER_NEAREST)
        return upscaled_image
