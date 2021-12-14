
import json
import logging
from argparse import ArgumentParser

import pygame

from mazeutils.maze import Maze, ChessObject


imgfilename = 'doraemon.jpeg'



def play_game(maze_config):
    # draw maze
    maze = Maze(maze_config)
    maze.draw()

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
                mouse_x, mouse_y = event.pos
                box_x, boy_y = maze.get_box_coordinates(mouse_x, mouse_y)
                print('{}, {}'.format(box_x, boy_y))
                for neighbor_x, neighbor_y in maze.valid_next_boxes(box_x, boy_y):
                    print('neighbor: {}, {}'.format(neighbor_x, neighbor_y))
                doraemon.move_to(box_x, boy_y)


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
