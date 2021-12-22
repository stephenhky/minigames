
import logging
import enum
from itertools import product
from collections import OrderedDict

import numpy as np
import pygame


def iterate_2d_neighbors(x, y):
    yield x-1, y
    yield x, y-1
    yield x+1, y
    yield x, y+1


class Direction(enum.Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    NODIRECTION = -1
    UNDEFINED = -2


def get_direction(prev_row, prev_col, next_row, next_col):
    if prev_col == next_col:
        if next_row > prev_row:
            return Direction.RIGHT
        elif next_row < prev_row:
            return Direction.LEFT
        else:
            return Direction.NODIRECTION
    elif prev_row == next_row:
        if next_col > prev_col:
            return Direction.DOWN
        elif next_col < prev_col:
            return Direction.UP
        else:
            return Direction.NODIRECTION
    else:
        return Direction.UNDEFINED


class Maze:
    def __init__(self, config, height=100, width=100, barrier_color=(255, 0, 0)):
        self.height = height
        self.width = width
        self.barrier_color = barrier_color

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

        self.screen = None

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

    def compute_box_screenpos(self, rowid, colid):
        return (2*rowid+1)*self.width // 2, (2*colid+1)*self.height // 2

    def draw(self):
        self.screen = pygame.display.set_mode((self.width * self.nbcols, self.height * self.nbrows))
        for [rowbarrierx, rowbarriery] in self.rowbarriers:
            pygame.draw.line(
                self.screen,
                self.barrier_color,
                (rowbarrierx * self.width, (rowbarriery + 1) * self.height),
                ((rowbarrierx + 1) * self.width, (rowbarriery + 1) * self.height)
            )
        for [colbarrierx, colbarriery] in self.colbarriers:
            pygame.draw.line(
                self.screen,
                self.barrier_color,
                ((colbarrierx + 1) * self.width, colbarriery * self.height),
                ((colbarrierx + 1) * self.width, (colbarriery + 1) * self.height)
            )

        # pygame.draw.line(screen, (0, 255, 0), (0, 1), (300, 400)) # for debug
        pygame.display.flip()

    def get_box_coordinates(self, mouse_x, mouse_y):
        return (mouse_x // self.height), (mouse_y // self.width)


class ChessObject:
    def __init__(self, imgfilepath, maze):
        self.maze = maze
        img = pygame.image.load(imgfilepath)
        img = pygame.transform.scale(img, (int(maze.width*0.9), int(maze.height*0.9)))
        img.convert()
        self.img = img
        self.rect = self.img.get_rect()
        self.loc = None

    def move_to(self, box_x, box_y):
        self.maze.screen.fill((0, 0, 0))
        self.maze.draw()
        screen_x, screen_y = self.maze.compute_box_screenpos(box_x, box_y)
        if self.loc is None:
            self.maze.screen.blit(self.img, self.rect)
            self.rect.center = screen_x, screen_y
            pygame.draw.rect(self.maze.screen, (0, 0, 0), self.rect, 1)
            pygame.display.update()
            self.loc = box_x, box_y
            print("entry loc"+str(self.loc))
        else:
            old_screen_x, old_screen_y = self.maze.compute_box_screenpos(self.loc[0], self.loc[1])
            screen_x, screen_y = self.maze.compute_box_screenpos(box_x, box_y)
            dx, dy = screen_x-old_screen_x, screen_y-old_screen_y
            self.rect.move_ip(dx, dy)
            self.maze.screen.blit(self.img, self.rect)
            pygame.display.flip()
            self.loc = box_x, box_y
            print("entry loc"+str(self.loc))


def initialize_probabilities_from_maze(maze):
    states = [
        (x, y)
        for x, y in product(range(maze.nbcols), range(maze.nbrows))
    ]
    P = OrderedDict()
    for x, y in states:
        P[(x, y)] = {}
        for newx, newy in maze.valid_next_boxes_iterator(x, y):
            direction = get_direction(x, y, newx, newy)
            P[(x, y)][direction] = [
                {
                    'state': (newx, newy),
                    'probability': 1.,
                    'reward': 0.,
                    'terminal': False
                }
            ]
    return P
