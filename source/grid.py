from pygame import draw, Surface, font
from . import uinput
from .node import Node, NODE_WIDTH, NODE_HEIGHT
from .astar import Astar, PATH_TILE, WALL_TILE, FINAL_PATH_TILE, START_TILE, END_TILE, TRAVELED_TILE, CURRENT_VISIT_TILE

DEFAULT_WIDTH = 20
DEFAULT_HEIGHT = 20

PATH_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 255)
FINAL_PATH_COLOR = (152, 0, 154)
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
TRAVELED_COLOR = (122, 203, 216)
CURRENT_VISIT_COLOR = (246, 31, 129)


class Grid:
    def __init__(self, w: int, h: int):
        self.width, self.height = w, h
        self.grid = [[Node(x, y) for x in range(self.width)] for y in range(self.height)]
        
        # rendering
        self.sprites = []
        self.font = None
        self.font_size = 11
        self.text_color = (255, 255, 255)

        # algorithm
        self.astar = Astar(self)

    def create(self):
        [self.sprites.append(Surface((NODE_WIDTH, NODE_HEIGHT), 0, 32).convert()) for i in range(7)]
        self.sprites[PATH_TILE].fill(PATH_COLOR)
        self.sprites[WALL_TILE].fill(WALL_COLOR)
        self.sprites[FINAL_PATH_TILE].fill(FINAL_PATH_COLOR)
        self.sprites[START_TILE].fill(START_COLOR)
        self.sprites[END_TILE].fill(END_COLOR)
        self.sprites[TRAVELED_TILE].fill(TRAVELED_COLOR)
        self.sprites[CURRENT_VISIT_TILE].fill(CURRENT_VISIT_COLOR)
        # load font
        self.font = font.Font("assets/CONSOLA.TTF", self.font_size)

    def update(self):
        # check if astar is running
        if uinput.is_key_clicked(uinput.P_KEY):
            self.astar.start_search()
        elif self.astar.is_running:
            self.astar.next_step()
        elif self.astar.is_backing:
            self.astar.next_back()
        # reset the aster
        elif uinput.is_key_clicked(uinput.R_KEY):
            self.astar.reset()
        elif uinput.is_key_clicked(uinput.C_KEY):
            self.clear_map()
        elif uinput.is_mouse_clicked(1):
            mpos = uinput.get_mouse_pos()
            gpos = (mpos[0] // NODE_WIDTH, mpos[1] // NODE_HEIGHT)
            # start tile
            if uinput.is_key_press(uinput.A_KEY):
                self.astar.set_start_tile(gpos)
            # end tile
            elif uinput.is_key_press(uinput.S_KEY):
                self.astar.set_end_tile(gpos)
            # wall tile
            else:
                self.set_node_type(gpos[0], gpos[1], WALL_TILE if self.get_node(gpos[0], gpos[1]).type != WALL_TILE else PATH_TILE)

    def render(self, window):
        for x in range(self.width):
            for y in range(self.height):
                node = self.get_node(x, y)
                window.blit(self.sprites[node.type], node.pos)
                # render some stats
                window.blit(self.font.render(f"{node.get_g():.2f}", False, self.text_color), (node.pos[0], node.pos[1] + 5))
                window.blit(self.font.render(f"{node.get_h():.2f}", False, self.text_color), (node.pos[0], node.pos[1] + 15))

    def get_node(self, x: int, y: int):
        return self.grid[y][x]
    
    def set_node_type(self, x: int, y: int, t: int):
        self.grid[y][x].type = t

    def clear_map(self):
        [[self.get_node(x, y).reset() for x in range(self.width)] for y in range(self.height)]
