
import logging

import pygame


def iterate_2d_neighbors(x, y):
    yield x-1, y
    yield x, y-1
    yield x+1, y
    yield x, y+1


class Maze:
    def __init__(self, config, height=100, width=100, barrier_color = (255, 0, 0)):
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

    def move_to(self, box_x, boy_y):
        rect = self.img.get_rect()
        self.maze.screen.blit(self.img, rect)
        screen_x, screen_y = self.maze.compute_box_screenpos(box_x, boy_y)
        rect.center = screen_x, screen_y
        pygame.draw.rect(self.maze.screen, (0, 0, 0), rect, 1)
        pygame.display.update()

