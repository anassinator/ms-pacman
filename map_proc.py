# -*- coding: utf-8 -*-

import numpy as np
from collections import deque
from game_map_objects import GameMapObjects


def get_slice(game_map, pac_pos, radius):
    """Extracts a slice of the map centered on Ms.Pacman.

    Args:
        game_map: Map matrix.
        pac_pos: Ms.Pacman position in matrix.
        radius: Radius of slice.

    Returns:
        Slice matrix.

    Deleted Parameters:
        map: Map matrix.
    """
    min_i = pac_pos[0] - radius
    max_i = pac_pos[0] + radius + 1
    min_j = pac_pos[1] - radius
    max_j = pac_pos[1] + radius + 1

    vertical_slice = slice(max(min_i, 0), min(max_i, game_map.HEIGHT))
    horizontal_slice = slice(max(min_j, 0), min(max_j, game_map.WIDTH))
    map_slice = game_map.map[vertical_slice, horizontal_slice]

    # Concatenate the opposite side of the board for a horizontal overflow.
    if min_j < 0:
        map_slice = np.hstack((
            game_map.map[vertical_slice, min_j - 1:-1],
            map_slice
        ))
    elif max_j >= game_map.WIDTH:
        map_slice = np.hstack((
            map_slice,
            game_map.map[vertical_slice, 0:max_j - game_map.WIDTH]
        ))

    # Concatenate walls for any vertical overflow.
    height, width = map_slice.shape
    if min_i < 0:
        map_slice = np.vstack((
            np.ones((abs(min_i), width), dtype=np.uint8),
            map_slice
        ))
    elif max_i >= game_map.HEIGHT:
        map_slice = np.vstack((
            map_slice,
            np.ones((max_i - game_map.HEIGHT, width), dtype=np.uint8)
        ))

    return hide_cells_behind_wall(map_slice)


def hide_cells_behind_wall(map_slice):
    """Hides cells which cannot be reached by Ms. PacMan.

    Args:
        map_slice: Map slice matrix.

    Returns:
        Map slice with cells that cannot be reached emptied.
    """
    height, width = map_slice.shape
    center = (height - 1) / 2

    # One is the same as GameMapObjects.WALL.
    shadowed_map = np.ones((height, width))
    visited = np.zeros((height, width))
    neighbor_queue = deque()
    neighbor_queue.append((center, center))

    while neighbor_queue:
        cell = neighbor_queue.popleft()
        visited[cell] = 1
        shadowed_map[cell] = map_slice[cell]
        if map_slice[cell] == GameMapObjects.WALL:
            continue
        for neighbor in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            i = cell[0] + neighbor[0]
            j = cell[1] + neighbor[1]
            if 0 <= i < height and 0 <= j < width and not visited[(i, j)]:
                neighbor_queue.append((i, j))

    return shadowed_map
