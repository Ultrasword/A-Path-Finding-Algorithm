import pygame

MOUSE_LEFT_CLICK = 1
MOUSE_RIGHT_CLICK = 3
MOUSE_SCROLL_WHEEL_CLICK = 2

# specific to a-star this time
A_KEY = pygame.K_a
S_KEY = pygame.K_s
P_KEY = pygame.K_p
R_KEY = pygame.K_r
C_KEY = pygame.K_c


mouse_pressed = [False for i in range(10)]
mouse_clicked = set()

get_mouse_pos = pygame.mouse.get_pos

def is_mouse_press(button: int):
    return mouse_pressed[button]

def is_mouse_clicked(button: int):
    return button in mouse_clicked


key_pressed = {}
key_clicked = set()

def is_key_press(button: int):
    return key_pressed.get(button)

def is_key_clicked(button: int):
    return button in key_clicked


