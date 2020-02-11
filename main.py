from pyglet.gl import *
from pyglet.window import key, mouse

from boids.window import Window
from boids.initialize import setup_gl


def main():
    window = Window(width=800, height=600, caption='Pyglet', resizable=True)
    window.set_exclusive_mouse(True)
    setup_gl()
    pyglet.app.run()


if __name__ == '__main__':
    main()
