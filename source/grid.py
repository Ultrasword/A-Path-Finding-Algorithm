import pygame
import math
from . import uin

from queue import PriorityQueue
from collections import deque


PATH_TYPE = 0
WALL_TYPE = 1

VISITED_TYPE = 2
FINAL_TYPE = 3

START_TYPE = 4
END_TYPE = 5

CHECKING_TYPE = 6

PATH_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 255)
VISIT_COLOR = (100, 100, 100)
FINAL_COLOR = (250, 100, 255)
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
CHECK_COLOR = (255, 255, 0)


class Node:
    def __init__(self, x: int, y: int):
        self.g, self.h = 0, 0
        self.x, self.y = x, y
        self.dis = 0
        self.type = 0
        self.dead_end = False
        self.vis = False
        self.prev = None
    
    def get_coords(self):
        return (self.x, self.y)

    def calculate_distance_to(self, other_node):
        dx, dy = self.x - other_node.x, self.y - other_node.y
        return math.sqrt(dx*dx+dy*dy)
    
    def get_to_cost(self):
        return self.dis + self.h
    
    def get_from_cost(self):
        return self.g + self.dis

    def reset(self):
        self.g, self.h = 0, 0
        self.dis = 0
        self.dead_end = False
        self.vis = False
        self.prev = None
        if self.type == VISITED_TYPE or self.type == FINAL_TYPE:
            self.type = PATH_TYPE


class Grid:
    def __init__(self, grid_size: list, node_size: list):
        self.grid = [[Node(x, y) for x in range(grid_size[0])] for y in range(grid_size[1])]
        self.dim = grid_size
        self.node_dim = node_size
        self.is_searching = False
        self.is_backing = False

        # for rendering
        self.sprites = []

        # astar
        self.astar = None
        self.start_node = None
        self.end_node = None

    def create(self):
        [self.sprites.append(pygame.Surface(self.node_dim).convert()) for i in range(7)]
        self.sprites[0].fill(PATH_COLOR)
        self.sprites[1].fill(WALL_COLOR)
        self.sprites[2].fill(VISIT_COLOR)
        self.sprites[3].fill(FINAL_COLOR)
        self.sprites[4].fill(START_COLOR)
        self.sprites[5].fill(END_COLOR)
        self.sprites[6].fill(CHECK_COLOR)

        # create other stuff
        self.astar = A_Star()

    def update(self):
        if uin.is_keyboard_clicked(pygame.K_ESCAPE):
            # interrupt the astar
            self.astar.interrupt()
        elif self.is_searching:
            self.astar.next_step()
        elif self.is_backing:
            self.astar.next_back()
        elif uin.is_keyboard_clicked(pygame.K_r):
            self.reset()
        elif uin.is_keyboard_clicked(pygame.K_c):
            self.clean_grid()
        else:
            # get input and check for stuff
            mpos = pygame.mouse.get_pos()
            if uin.is_mouse_click(1):
                gpos = [mpos[0] // self.node_dim[0], mpos[1] // self.node_dim[1]]
                if uin.is_keyboard_button(pygame.K_a):
                    if self.start_node:
                        self.start_node.type = PATH_TYPE
                    self.set_node_type(gpos[0], gpos[1], START_TYPE)
                    self.start_node = self.get_node(gpos[0], gpos[1])
                elif uin.is_keyboard_button(pygame.K_s):
                    if self.end_node:
                        self.end_node.type = PATH_TYPE
                    self.set_node_type(gpos[0], gpos[1], END_TYPE)
                    self.end_node = self.get_node(gpos[0], gpos[1])
                else:
                    self.set_node_type(gpos[0], gpos[1], WALL_TYPE if self.get_node(gpos[0], gpos[1]).type == PATH_TYPE else PATH_TYPE)
            elif uin.is_keyboard_clicked(pygame.K_p):
                # start path finding from a to b
                self.reset()
                self.astar.starting(self)

    def render(self, window):
        for x in range(self.dim[0]):
            for y in range(self.dim[1]):
                node = self.get_node(x, y)
                window.blit(self.sprites[node.type], (node.x * self.node_dim[0], node.y * self.node_dim[1]))

    def get_node(self, x, y):
        return self.grid[y][x]
    
    def set_node_type(self, x, y, t):
        self.grid[y][x].type = t
    
    def reset(self):
        for x in range(self.dim[0]):
            for y in range(self.dim[1]):
                self.get_node(x, y).reset()
        self.astar.reset()

    def clean_grid(self):
        for x in range(self.dim[0]):
            for y in range(self.dim[1]):
                self.set_node_type(x, y, PATH_TYPE)


DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
MOVE_COST = 0.1


class A_Star:
    """
    Searches via the following format:
        - (cost, node_pos)
    """

    def __init__(self):
        self.grid = None
        self.start = None
        self.end = None
        self.aq = None
        self.cnode = None
    
    def starting(self, grid):
        self.grid = grid
        self.grid.is_searching = True
        # some starting variables
        self.aq = PriorityQueue()
        self.start = grid.start_node
        self.start.vis = True
        self.end = grid.end_node
        if not self.start or not self.end:
            print("Start and End node hav enot been placed!")
            self.grid.is_searching = False
        # add initial starting pos
        self.aq.put((0, self.start.get_coords()))
    
    def next_step(self):
        # start
        if not self.aq.empty():
            c = self.aq.get()
            cost, cnode = c[0], self.grid.get_node(c[1][0], c[1][1])
            if not cnode.vis:
                cnode.type = VISITED_TYPE
            cnode.vis = True
            cx, cy = cnode.get_coords()
            if (cx, cy) == self.end.get_coords():
                # found end
                print("-----Finished A*-----")
                cnode.type = END_TYPE
                self.grid.is_searching = False
                self.back()
                self.aq = None
                return

            possible_paths = []
            for mx, my in DIRECTIONS:
                nx, ny = cx + mx, cy + my
                if nx < 0 or nx >= self.grid.dim[0]:
                    continue
                if ny < 0 or ny >= self.grid.dim[1]:
                    continue
                if self.grid.get_node(nx, ny).type == WALL_TYPE or self.grid.get_node(nx, ny).vis:
                    continue
                possible_paths.append((nx, ny))
            # go through paths
            # first check if the next node has already been visited
            # if it has, then check which node should be used as parent node to minimize travel length
            for nx, ny in possible_paths:
                node = self.grid.get_node(nx, ny)
                if node.vis:
                    # check for better parent
                    if cnode.dis < node.prev.dis:
                        node.prev = cnode
                    continue
                else:
                    node.prev = cnode
                # if not visited, then travel down path
                node.dis = cnode.dis + MOVE_COST
                node.g = node.calculate_distance_to(self.start)
                node.h = node.calculate_distance_to(self.end)
                self.aq.put((node.get_to_cost(), node.get_coords()))
            if not possible_paths:
                self.next_back()
        # if it is empty
        else:
            print("Coult not reach ending node.")
            self.grid.is_searching = False
            self.reset()
    
    def next_back(self):
        if self.cnode.get_coords() != self.start.get_coords():
            # follow back the node.prev
            if self.cnode.type != END_TYPE:
                self.cnode.type = FINAL_TYPE
            if self.cnode.prev:
                self.cnode = self.cnode.prev
            else:
                print("-----Finished Backtrack-----")
                self.grid.is_backing = False
        else:
            self.grid.is_backing = False

    def back(self):
        self.grid.is_backing = True
        print("-----Starting BackTrack-----")
        self.aq = deque()
        self.cnode = self.grid.end_node

    def interrupt(self):
        if self.grid and self.grid.is_searching:
            self.grid.is_searching = False
            self.grid.is_backing = False
            self.reset()
        
    def reset(self):
        # clear grid of travelled nodes
        self.start = None
        self.end = None
        self.grid = None
        self.aq = None


