
mouse_button = {}
mouse_clicked = set()

keyboard_button = {}
keyboard_clicked = set()

def is_mouse_button(key):
    return mouse_button.get(key)

def is_mouse_click(key):
    return key in mouse_clicked

def is_keyboard_button(key):
    return keyboard_button.get(key)

def is_keyboard_clicked(key):
    return key in keyboard_clicked





