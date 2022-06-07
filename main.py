import pygame
from source import grid, uinput

FPS = 30
WINDOW_SIZE = (1280, 720)

GRID = grid.Grid(grid.DEFAULT_WIDTH, grid.DEFAULT_HEIGHT)
pygame.init()
window = pygame.display.set_mode((GRID.width * grid.NODE_WIDTH +100, 
GRID.height * grid.NODE_HEIGHT+2), 0, 32)
pygame.display.set_caption("A* Algorithm")
clock = pygame.time.Clock()

GRID.create()

running = True
while running:
    uinput.mouse_clicked.clear()
    uinput.key_clicked.clear()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            uinput.mouse_pressed[e.button] = True
            uinput.mouse_clicked.add(e.button)
        elif e.type == pygame.MOUSEBUTTONUP:
            uinput.mouse_pressed[e.button] = False
        elif e.type == pygame.KEYDOWN:
            uinput.key_pressed[e.key] = True
            uinput.key_clicked.add(e.key)
        elif e.type == pygame.KEYUP:
            uinput.key_pressed[e.key] = False
    
    GRID.update()
    GRID.render(window)

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
