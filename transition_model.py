# -*- coding: utf-8 -*-

from map_proc import get_slice


def get_next_state(game, action):
    move = game.action_to_move(action)
    new_pos = game.get_next_position(move)
    return get_slice(game.map, new_pos, 2)
