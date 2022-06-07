from math import sqrt

NODE_WIDTH = 50
NODE_HEIGHT = 50


TO_WEIGHT = [0.4, 0.6]
FROM_WEIGHT = [0.6, 0.4]


class Node:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y
        self.pos = (self.x * NODE_WIDTH, self.y * NODE_HEIGHT)
        self.type = 0
        # stats
        self.dis_from_start = 0
        self.g, self.h = 0, 0
        self.came_from = None
        self.dead_end = False
        self.possible_paths = 0
        self.visited = False
        self.in_queue = False

    def get_g(self):
        return self.g
    
    def get_h(self):
        return self.h
    
    def reset(self):
        self.clean()
        self.type = 0
    
    def clean(self):
        self.dis_from_start = 0
        self.g, self.h = 0, 0
        self.came_from = None
        self.dead_end = False
        self.possible_paths = 0
        self.visited = False
        self.in_queue = False

    def get_dis_from(self, other):
        dx, dy = other.x - self.x, other.y - self.y
        return sqrt(dx*dx+dy*dy)

    def set_dead_end(self):
        self.dead_end = True
        # recursive
        if self.came_from:
            self.came_from.set_dead_end()
    
    def get_grid_pos(self):
        return self.x, self.y

    def get_to_cost(self):
        return self.g * TO_WEIGHT[0] + self.h * TO_WEIGHT[1]
    
    def get_from_cost(self):
        return self.g * FROM_WEIGHT[0] + self.h * FROM_WEIGHT[1]

