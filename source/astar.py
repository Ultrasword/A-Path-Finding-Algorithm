
from queue import PriorityQueue

PATH_TILE = 0
WALL_TILE = 1
FINAL_PATH_TILE = 2
START_TILE = 3
END_TILE = 4
TRAVELED_TILE = 5
CURRENT_VISIT_TILE = 6



MOVE_COST = 1
DIRECTIONS = ((1,0), (-1, 0), (0, 1), (0, -1))

class Astar:
    def __init__(self, grid_object):
        self.grid = grid_object
        # toggles
        self.is_running = False
        self.is_backing = False
        # important tiles
        self.start = None
        self.end = None
        self.cnode = None
        self.aq = None
        self.prev_node_render = None
        self.prev_node_type = None

    def set_start_tile(self, coords: list):
        if self.start:
            self.start.type = PATH_TILE
        self.start = self.grid.get_node(coords[0], coords[1])
        self.start.type = START_TILE
    
    def set_end_tile(self, coords: list):
        if self.end:
            self.end.type = PATH_TILE
        self.end = self.grid.get_node(coords[0], coords[1])
        self.end.type = END_TILE

    def reset(self):
        # reset the search --> as in reset all visited tiles to path tiles
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                node = self.grid.get_node(x, y)
                if node.type == TRAVELED_TILE or node.type == FINAL_PATH_TILE:
                    node.type = PATH_TILE
                node.clean()

    def start_search(self):
        if self.is_running:
            self.next_step()
            return
        elif self.is_backing:
            self.next_back()
            return
        # we init the search process
        if not self.start or not self.end:
            return print("-----[A* problem] Start or End not set!-----")
        # reset the items
        self.reset()
        # set the cnode
        self.cnode = self.start
        self.aq = PriorityQueue()
        # how to put in 
        # we will determine the next path by choosing
        self.cnode.h = self.cnode.get_dis_from(self.end)
        self.aq.put((self.cnode.h, self.cnode.get_grid_pos()))
        self.prev_node_render = self.start
        self.prev_node_type = self.start.type
        self.start.type = CURRENT_VISIT_TILE
        self.is_running = True
        self.start.in_queue = True
        print("-----Starting A* Path Finder-----")

    def next_step(self):
        if self.aq:
            # reset previous node
            self.prev_node_render.type = TRAVELED_TILE if self.prev_node_type != START_TILE else self.prev_node_type
            # continue
            c = self.aq.get()
            pcost, cnode = c[0], self.grid.get_node(c[1][0], c[1][1])
            cnode.in_queue = False
            if c[1] == self.end.get_grid_pos():
                self.is_running = False
                print("-----Found End-----")
                self.aq = None
                return
            cnode.dis_from_start += MOVE_COST
            cnode.visited = True
            # set prev node
            self.prev_node_type = cnode.type
            self.prev_node_render = cnode
            if cnode.type != START_TILE:
                cnode.type = CURRENT_VISIT_TILE
            # find possible paths
            possible = self.find_possible_paths(cnode)
            for nnode in possible:
                # calculate the g and h
                # g: dis from start
                # h: dis from end
                nnode.g = self.start.get_dis_from(nnode)
                nnode.h = self.end.get_dis_from(nnode)
                if nnode.visited:
                    if nnode.dis_from_start > cnode.dis_from_start + MOVE_COST:
                        nnode.dis_from_start = cnode.dis_from_start + MOVE_COST
                        nnode.came_from = cnode
                else:
                    nnode.dis_from_start = cnode.dis_from_start + MOVE_COST
                    nnode.came_from = cnode
                    if nnode.in_queue:
                        continue
                    nnode.in_queue = True
                    self.aq.put((nnode.get_to_cost(), nnode.get_grid_pos()))

    """Checks if vis, if wall, if deadend"""
    def find_possible_paths(self, node):
        results = []
        for mx, my in DIRECTIONS:
            nx, ny = node.x + mx, node.y + my
            # check if out of bounds
            if nx < 0 or nx >= self.grid.width:
                continue
            if ny < 0 or ny >= self.grid.height:
                continue
            # check if already visited
            nnode = self.grid.get_node(nx, ny)
            # check if visited or is a wall or a dead end
            if nnode.visited or nnode.type == WALL_TILE or nnode.dead_end:
                continue
            # add to the results
            results.append(nnode)
        node.possible_paths = len(results)
        # set a bunch of dead ends
        # dead end is when no paths + every recursive path behind has 1 possible path
        print(f"{node.x}, {node.y} | Possible Paths: {node.possible_paths}")
        if node.possible_paths == 0:
            # recursively go back and check
            node.set_dead_end()
        return results

    def backtrack(self):
        # TODO - backtrack
        pass

    def next_back(self):
        pass






