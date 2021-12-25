
import json
import logging
from argparse import ArgumentParser
from itertools import product

import pygame
import numpy as np
from scipy.spatial.distance import euclidean

from mazeutils.maze import Maze, ChessObject, initialize_probabilities_from_maze, Direction
from mdputils import value_iteration, policy_iteration, make_state_action_dicts


imgfilename = 'doraemon.jpeg'


def play_game(maze_config, approach, gamma=0.75):
    # draw maze
    maze = Maze(maze_config)
    maze.draw()

    # initial_weights
    maxdistance = euclidean(np.zeros(2), np.array([maze.nbrows-1, maze.nbcols-1]))
    P = initialize_probabilities_from_maze(maze)
    for x, y in product(range(maze.nbcols), range(maze.nbrows)):
        for direction in P[(x, y)]:
            if P[(x, y)][direction][0]['state'] == (maze.nbcols - 1, maze.nbrows - 1):
                P[(x, y)][direction][0]['terminal'] = True
                P[(x, y)][direction][0]['reward'] = 100.0
            else:
                # NOTE: This kind of distance reward will make Doraemon trapped in an infinite loop.
                # newx, newy = P[(x, y)][direction][0]['state']
                # distance = euclidean(np.array([maze.nbrows-1, maze.nbcols-1]), np.array([newx, newy]))
                # P[(x, y)][direction][0]['reward'] = 1.0 - distance / maxdistance
                pass
    print(P)

    # drawing image
    doraemon = ChessObject('doraemon.jpeg', maze)
    doraemon.move_to(0, 0)

    # calculating value function
    stateindexdict, actionindexdict = make_state_action_dicts(P)
    if approach == 'policy':
        V, pi = policy_iteration(P, gamma=gamma, stateindexdict=stateindexdict, actionindexdict=actionindexdict)
    elif approach == 'value':
        V, pi = value_iteration(P, gamma=gamma, stateindexdict=stateindexdict, actionindexdict=actionindexdict)
    else:
        raise Exception('This block should be unreachable!')
    print(V)
    for state in stateindexdict.keys():
        print('({}, {}): {}'.format(state[0], state[1], pi(state)))

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
    argparser.add_argument('--gamma', type=float, default=0.75, help='discount factor (default: 0.75)')
    return argparser


if __name__ == '__main__':
    args = get_argparser().parse_args()
    maze_config = json.load(open(args.mazejson, 'r'))
    approach = args.approach
    if not approach in ['policy', 'value']:
        raise ValueError('approach has to be either "policy" or "value", not {}.'.format(approach))
    gamma = args.gamma

    pygame.init()
    play_game(maze_config, approach, gamma=gamma)
    pygame.quit()
