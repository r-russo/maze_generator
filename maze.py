import pyglet

GRID_SIZE = 32
WIDTH = 20
HEIGHT = 10
MARGIN = 50

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {}
        self.walls['N'] = True
        self.walls['E'] = True
        self.walls['S'] = True
        self.walls['W'] = True

    def draw(self):
        if self.walls['N']:
            coordsN = (self.x, self.y, self.x + 1, self.y)
            coordsN = [i*GRID_SIZE+MARGIN//2 for i in coordsN]
        if self.walls['E']:
            coordsE = (self.x + 1, self.y, self.x + 1, self.y + 1)
            coordsE = [i*GRID_SIZE+MARGIN//2 for i in coordsE]
        if self.walls['S']:
            coordsS = (self.x, self.y + 1, self.x + 1, self.y + 1)
            coordsS = [i*GRID_SIZE+MARGIN//2 for i in coordsS]
        if self.walls['W']:
            coordsW = (self.x, self.y, self.x, self.y + 1)
            coordsW = [i*GRID_SIZE+MARGIN//2 for i in coordsW]
        pyglet.graphics.draw(8, pyglet.gl.GL_LINES,
                             ('v2i', coordsN + coordsE + coordsS + coordsW))

cells = []
for i in range(WIDTH):
    for j in range(HEIGHT):
        cells.append(Cell(i, j))

window = pyglet.window.Window(WIDTH*GRID_SIZE + MARGIN,
                              HEIGHT*GRID_SIZE + MARGIN)

@window.event
def on_draw():
    window.clear()
    for cell in cells:
        cell.draw()

pyglet.app.run()
