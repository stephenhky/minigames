
import json
import logging

import numpy as np
import pygame


class Maze:
    def __init__(self, config):
        self.nbrows = config['nbrows']
        self.nbcols = config['nbcols']
        self.rowbarriers = np.array(config.get('rowbarriers', [[]]))
        self.colbarriers = np.array(config.get('colbarriers', [[]]))

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

    def valid_next_box(self, rowid, colid):
        pass


def draw_maze(maze):
    pass