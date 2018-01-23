import pyglet
from maze import Maze

class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(500, 500)
        self.maze = Maze(self.get_size()[0], self.get_size()[1], 32)
        pyglet.clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        self.maze.update()

    def on_draw(self):
        self.clear()
        self.maze.draw()

if __name__ == '__main__':
    window = Window()
    pyglet.app.run()
