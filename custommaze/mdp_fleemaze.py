
import json
import logging
from argparse import ArgumentParser
from itertools import product

import pygame

from mazeutils.maze import Maze, ChessObject, initialize_probabilities_from_maze


imgfilename = 'doraemon.jpeg'


def play_game(maze_config):
    # draw maze
    maze = Maze(maze_config)
    maze.draw()

    # initial_weights
    P = initialize_probabilities_from_maze(maze, weight_initialization='uniform')
    for x, y in product(range(maze.nbcols), range(maze.nbrows)):
        for direction in P[(x, y)]:
            if P[(x, y)][direction]['state'] == (maze.nbcols - 1, maze.nbrows - 1):
                P[(x, y)][direction]['terminal'] = True
                P[(x, y)][direction]['reward'] = 1.0
    print(P)

    # drawing image
    doraemon = ChessObject('doraemon.jpeg', maze)
    doraemon.move_to(0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            logging.debug(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                # move doraemon with reinforcement learning
                pass


def get_argparser():
    argparser = ArgumentParser(description='Draw maze and click')
    argparser.add_argument('mazejson', help='path of maze configuration JSON file')
    return argparser


if __name__ == '__main__':
    args = get_argparser().parse_args()
    maze_config = json.load(open(args.mazejson, 'r'))

    pygame.init()
    play_game(maze_config)
    pygame.quit()
