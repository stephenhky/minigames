
import json
import logging

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
        if not (np.all(self.rowbarriers[:, 0] < self.nbrows-1) or np.all(self.rowbarriers[:, 1] < self.nbcols)):
            for rowx, rowy in self.rowbarriers:
                if rowx < self.nbrows-1 and rowy < self.nbcols:
                    valid = False
                    logging.error('Invalid row barriers: ({},  {})'.format(rowx, rowy))
        if not (np.all(self.colbarriers[:, 0] < self.nbrows) or np.all(self.colbarriers[:, 1] < self.nbcols-1)):
            for colx, coly in self.colbarriers:
                if colx < self.nbrows-1 and coly < self.nbcols:
                    valid = False
                    logging.error('Invalid row barriers: ({},  {})'.format(colx, coly))
        if not valid:
            raise ValueError('Invalid barriers!')

    def valid_next_boxes_iterator(self, rowid, colid):
        for x, y in iterate_2d_neighbors(rowid, colid):
            if x >= 0 and x < self.nbrows and y >= 0 and y < self.nbcols:
                if y == colid:
                    if x - rowid == 1:
                        if not [rowid, colid] in self.rowbarriers:
                            yield x, y
                    elif x - rowid == -1:
                        if not [rowid-1, colid] in self.rowbarriers:
                            yield x, y
                    else:
                        logging.warning('Not reachable!')
                elif x == rowid:
                    if y - colid == 1:
                        if not [rowid, colid] in self.colbarriers:
                            yield x, y
                    elif y - colid == -1:
                        if not [rowid, colid-1] in self.colbarriers:
                            yield x, y
                    else:
                        logging.warning('Not reachable!')
                else:
                    logging.warning('Not reachanle!')

    def valid_next_boxes(self, rowid, colid):
        return [[x, y] for x, y in self.valid_next_boxes_iterator(rowid, colid)]




def draw_maze(maze):
    pass