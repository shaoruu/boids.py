from pyglet.gl import *
from pyglet.window import key, mouse

from boids.main import Main
from boids.initialize import setup_gl


def main():
    boids = Main(width=800, height=600, caption='Pyglet', resizable=True)
    boids.set_exclusive_mouse(True)
    setup_gl()
    pyglet.app.run()


if __name__ == '__main__':
    main()
