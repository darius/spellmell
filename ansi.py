"""
ANSI terminal control
"""

ansi = '\x1b['

black, red, green, yellow, blue, magenta, cyan, white, default_color = range(9)

def bright(color):
    return 60 + color

def set_foreground(color):
    return (ansi + '%dm') % (30 + color)

def set_background(color):
    return (ansi + '%dm') % (40 + color)
