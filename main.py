import pygame
pygame.init()

from source import grid, uin


FPS = 30
GRID_SIZE = (20, 20)
TILE_SIZE = (30, 30)

window = pygame.display.set_mode((GRID_SIZE[0] * TILE_SIZE[0], GRID_SIZE[1] * TILE_SIZE[1]), 0, 32)
clock = pygame.time.Clock()

GRID = grid.Grid(GRID_SIZE, TILE_SIZE)
GRID.create()



running = True
while running:
    uin.keyboard_clicked.clear()
    uin.mouse_clicked.clear()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            uin.keyboard_button[e.key] = True
            uin.keyboard_clicked.add(e.key)
        elif e.type == pygame.KEYUP:
            uin.keyboard_button[e.key] = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            uin.mouse_button[e.button] = True
            uin.mouse_clicked.add(e.button)
        elif e.type == pygame.MOUSEBUTTONUP:
            uin.mouse_button[e.button] = False
    
    GRID.update()
    GRID.render(window)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
