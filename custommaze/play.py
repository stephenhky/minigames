
import json
import logging
from argparse import ArgumentParser

import numpy as np
import pygame


def iterate_2d_neighbors(x, y):
    yield x-1, y
    yield x, y-1
    yield x+1, y
    yield x, y+1


class Maze:
    def __init__(self, config):
        self.nbrows = config['nbrows']
        self.nbcols = config['nbcols']
        self.rowbarriers = config.get('rowbarriers', [[]])
        self.colbarriers = config.get('colbarriers', [[]])

        # validate
        valid = True
        for [x, y] in self.rowbarriers:
            if not (x < self.nbcols and y < self.nbrows-1):
                valid = False
                logging.error('Invalid row barriers: ({},  {})'.format(x, y))
        for [x, y] in self.colbarriers:
            if not (x < self.nbcols-1 and y < self.nbrows):
                valid = False
                logging.error('Invalid column barriers: ({},  {})'.format(x, y))
        if not valid:
            raise ValueError('Invalid barriers!')

    def valid_next_boxes_iterator(self, rowid, colid):
        for x, y in iterate_2d_neighbors(rowid, colid):
            if x >= 0 and x < self.nbcols and y >= 0 and y < self.nbrows:
                if y == colid:
                    if x - rowid == 1:
                        if not [rowid, colid] in self.colbarriers:
                            yield x, y
                    elif x - rowid == -1:
                        if not [rowid-1, colid] in self.colbarriers:
                            yield x, y
                    else:
                        logging.warning('Not reachable!')
                elif x == rowid:
                    if y - colid == 1:
                        if not [rowid, colid] in self.rowbarriers:
                            yield x, y
                    elif y - colid == -1:
                        if not [rowid, colid-1] in self.rowbarriers:
                            yield x, y
                    else:
                        logging.warning('Not reachable!')
                else:
                    logging.warning('Not reachanle!')

    def valid_next_boxes(self, rowid, colid):
        return [[x, y] for x, y in self.valid_next_boxes_iterator(rowid, colid)]




def draw_maze(maze, height=100, width=100):
    barrier_color = (255, 0, 0)
    screen = pygame.display.set_mode((width*maze.nbcols, height*maze.nbrows))
    for [rowbarrierx, rowbarriery] in maze.rowbarriers:
        pygame.draw.line(
            screen,
            barrier_color,
            (rowbarrierx*width, (rowbarriery+1)*height),
            ((rowbarrierx+1)*width, (rowbarriery+1)*height)
        )
    for [colbarrierx, colbarriery] in maze.colbarriers:
        pygame.draw.line(
            screen,
            barrier_color,
            ((colbarrierx+1)*width, colbarriery*height),
            ((colbarrierx+1)*width, (colbarriery+1)*height)
        )

    # pygame.draw.line(screen, (0, 255, 0), (0, 1), (300, 400)) # for debug
    pygame.display.flip()


def get_argparser():
    argparser = ArgumentParser(description='Draw maze')
    argparser.add_argument('mazejson', help='path of maze configuration JSON file')
    return argparser


if __name__ == '__main__':
    args = get_argparser().parse_args()
    maze_config = json.load(open(args.mazejson, 'r'))

    maze = Maze(maze_config)

    pygame.init()

    draw_maze(maze)
    running = True
    while running:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
