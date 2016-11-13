# -*- coding: utf-8 -*-

from map_proc import get_slice


def get_next_position(game, action):
    move = [(-1, 0), (0, 1), (0, -1), (1, 0)][action - 2]
    return (
        game.ms_pacman_position[0] + move[0],
        game.ms_pacman_position[1] + move[1]
    )


def get_next_state(game, action):
    new_pos = get_next_position(game, action)
    return get_slice(game.map, new_pos, 2)
