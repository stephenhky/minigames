
import json
import logging
from argparse import ArgumentParser
from itertools import product

import pygame

from mazeutils.maze import Maze, ChessObject, initialize_probabilities_from_maze, Direction
from mdputils import value_iteration, policy_iteration, make_state_action_dicts


imgfilename = 'doraemon.jpeg'


def play_game(maze_config, approach):
    # draw maze
    maze = Maze(maze_config)
    maze.draw()

    # initial_weights
    P = initialize_probabilities_from_maze(maze)
    for x, y in product(range(maze.nbcols), range(maze.nbrows)):
        for direction in P[(x, y)]:
            if P[(x, y)][direction][0]['state'] == (maze.nbcols - 1, maze.nbrows - 1):
                P[(x, y)][direction][0]['terminal'] = True
                P[(x, y)][direction][0]['reward'] = 1.0
    print(P)

    # drawing image
    doraemon = ChessObject('doraemon.jpeg', maze)
    doraemon.move_to(0, 0)

    # calculating value function
    stateindexdict, actionindexdict = make_state_action_dicts(P)
    if approach == 'policy':
        V, pi = policy_iteration(P, stateindexdict=stateindexdict, actionindexdict=actionindexdict)
    elif approach == 'value':
        V, pi = value_iteration(P, stateindexdict=stateindexdict, actionindexdict=actionindexdict)
    else:
        raise Exception('This block should be unreachable!')

    # looping
    running = True
    while running:
        for event in pygame.event.get():
            logging.debug(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                # move doraemon with reinforcement learning
                x, y = doraemon.loc
                direction = pi((x, y))
                if direction == Direction.LEFT:
                    x -= 1
                elif direction == Direction.RIGHT:
                    x += 1
                elif direction == Direction.UP:
                    y -= 1
                elif direction == Direction.DOWN:
                    y += 1
                else:
                    raise Exception('Direction? {}'.format(direction))
                doraemon.move_to(x, y)


def get_argparser():
    argparser = ArgumentParser(description='Draw maze and click')
    argparser.add_argument('mazejson', help='path of maze configuration JSON file')
    argparser.add_argument('approach', type=str, help='approach (option: "policy" for policy iteration, and "value" for value iteration)')
    return argparser


if __name__ == '__main__':
    args = get_argparser().parse_args()
    maze_config = json.load(open(args.mazejson, 'r'))
    approach = args.approach
    if not approach in ['policy', 'value']:
        raise ValueError('approach has to be either "policy" or "value", not {}.'.format(approach))

    pygame.init()
    play_game(maze_config, approach)
    pygame.quit()
