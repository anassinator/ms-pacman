# -*- coding: utf-8 -*-

from map_proc import get_slice
from game_map import GameMap
from game_map_objects import GameMapObjects, Ghost


def get_next_state(game, action):
    move = game.action_to_move(action)
    new_pos = game.get_next_position(game.ms_pacman_position, move)
    game_map = GameMap.from_map(game._blank_map.map.copy())
    if game.fruit.exists:
        game_map.map[game.fruit.position] = GameMapObjects.FRUIT
    for ghost in game.ghosts:
        new_ghost_position = game.get_next_position(ghost.position,
                                                    ghost.direction)
        if (not 0 < new_ghost_position[0] < game_map.HEIGHT or
                not 0 < new_ghost_position[1] < game_map.WIDTH or
                ghost.position == new_pos):
            if ghost.state == Ghost.GOOD:
                game_map.map[ghost.position] = GameMapObjects.GOOD_GHOST
            elif ghost.state == Ghost.BAD:
                game_map.map[ghost.position] = GameMapObjects.BAD_GHOST
        elif game_map.map[new_ghost_position] == GameMapObjects.WALL:
            continue
        elif ghost.state == Ghost.GOOD:
            game_map.map[new_ghost_position] = GameMapObjects.GOOD_GHOST
        elif ghost.state == Ghost.BAD:
            game_map.map[new_ghost_position] = GameMapObjects.BAD_GHOST
    return get_slice(game_map, new_pos, 2)
