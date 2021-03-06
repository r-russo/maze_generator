import pyglet
import random

class Cell:
    def __init__(self, x, y, exit=None):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {}
        self.walls['N'] = True
        self.walls['E'] = True
        self.walls['S'] = True
        self.walls['W'] = True

        if exit is not None:
            print(self.x, self.y)
            self.walls[exit] = False

class Maze:
    def __init__(self, width, height, cell_size):
        self.cell_size = cell_size
        self.height = height//cell_size
        self.width = width//cell_size
        self.margin_left = (width - self.width*cell_size)//2
        self.margin_top = (height - self.height*cell_size)//2
        self.cells = []

        # generate random exit
        if random.random() > 0.5:  # left side
            exit1_i = 0
            exit1_j = random.randint(0, self.height - 1)
            exit1 = 'E'
        else:  # bottom
            exit1_i = self.width - 1
            exit1_j = 0
            exit1 = 'S'

        exit_coord = exit1_i + exit1_j*self.width
        for j in range(self.height):
            for i in range(self.width):
                if i == exit1_i and j == exit1_j:
                    self.cells.append(Cell(i, j, exit1))
                else:
                    self.cells.append(Cell(i, j))
        self.cells[exit_coord].visited = True
        self.stack = [exit_coord]
        self.done = False

    def update(self):
        # (0, 0) is lower left for cell in self.cells:
        # check neighbors
        if self.done:
            return
        neighbors = []

        # Check that current_cell is not on the left side
        if not self.stack[-1] % self.width == 0:
            if not self.cells[self.stack[-1] - 1].visited:
                neighbors.append(self.stack[-1] - 1)

        # Not in the top row
        if not self.stack[-1] >= self.width * (self.height - 1):
            if not self.cells[self.stack[-1] + self.width].visited:
                neighbors.append(self.stack[-1] + self.width)

        # Not on the right side
        if not (self.stack[-1] + 1) % self.width == 0 or \
           self.stack[-1] == 0:
            if not self.cells[self.stack[-1] + 1].visited:
                neighbors.append(self.stack[-1] + 1)

        # Not in the bottom row
        if not self.stack[-1] < self.width:
            if not self.cells[self.stack[-1] - self.width].visited:
                neighbors.append(self.stack[-1] - self.width)

        if neighbors == []:
            self.stack.pop()
            if self.stack == []:
                self.stack = [0]
                self.done = True
        else:
            next_cell = neighbors[random.randint(0, len(neighbors) - 1)]

            self.stack.append(next_cell)
            self.stack[-1] = int(next_cell)
            self.cells[self.stack[-1]].visited = True

            # Open walls
            # Next cell is either up or right
            if self.stack[-1] - self.stack[-2] > 0:
                # Next cell is right
                if self.stack[-1] - 1 == self.stack[-2]:
                    self.cells[self.stack[-1]].walls['W'] = False
                    self.cells[self.stack[-2]].walls['E'] = False
                else:
                    self.cells[self.stack[-1]].walls['S'] = False
                    self.cells[self.stack[-2]].walls['N'] = False
            else:
                if self.stack[-1] + 1 == self.stack[-2]:
                    self.cells[self.stack[-1]].walls['E'] = False
                    self.cells[self.stack[-2]].walls['W'] = False
                else:
                    self.cells[self.stack[-1]].walls['N'] = False
                    self.cells[self.stack[-2]].walls['S'] = False

    def draw(self):
        batch = pyglet.graphics.Batch()
        for ix, cell in enumerate(self.cells):
            vertices = 0
            if cell.walls['N']:
                coordsN = (cell.x, cell.y + 1, cell.x + 1, cell.y + 1)
                coordsN = [i*self.cell_size + self.margin_top
                           for i in coordsN]
                vertices += 2
            else:
                coordsN = []
            if cell.walls['E']:
                coordsE = (cell.x + 1, cell.y, cell.x + 1, cell.y + 1)
                coordsE = [i*self.cell_size + self.margin_top
                           for i in coordsE]
                vertices += 2
            else:
                coordsE = []
            if cell.walls['S']:
                coordsS = (cell.x, cell.y, cell.x + 1, cell.y)
                coordsS = [i*self.cell_size + self.margin_top
                           for i in coordsS]
                vertices += 2
            else:
                coordsS = []
            if cell.walls['W']:
                coordsW = (cell.x, cell.y, cell.x, cell.y + 1)
                coordsW = [i*self.cell_size + self.margin_top
                           for i in coordsW]
                vertices += 2
            else:
                coordsW = []

            coordsRect = (cell.x, cell.y,
                          cell.x + 1, cell.y,
                          cell.x + 1, cell.y + 1,
                          cell.x, cell.y + 1)
            coordsRect = [i*self.cell_size + self.margin_top
                          for i in coordsRect]
            color = (255, 255, 255) * vertices
            color_visit = (50, 100, 50) * 4
            color_current = (100, 200, 100) * 4

            if ix == self.stack[-1]:
                batch.add(4, pyglet.gl.GL_QUADS, None,
                          ('v2i', coordsRect),
                          ('c3B', color_current))
            elif cell.visited:
                batch.add(4, pyglet.gl.GL_QUADS, None,
                          ('v2i', coordsRect),
                          ('c3B', color_visit))
            batch.add(vertices, pyglet.gl.GL_LINES, None,
                      ('v2i', coordsN + coordsE + coordsS + coordsW),
                      ('c3B', color))
        batch.draw()

