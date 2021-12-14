
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
                print('clickpos: {}, {}'.format(box_x, boy_y))
                img_box_x, img_box_y = doraemon.loc
                print(maze.valid_next_boxes(img_box_y, img_box_y))
                if [box_x, boy_y] in maze.valid_next_boxes(img_box_x, img_box_y):
                    doraemon.move_to(box_x, boy_y)
                else:
                    print('Not allowed')
                print('doraemon pos: {}, {}'.format(*doraemon.loc))


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
