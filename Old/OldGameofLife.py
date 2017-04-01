""" Rules  of Conwell's game of life:
    - Any live cell with under 2 live neighbours dies from exposure
    - Any live cell with over 3 live neighbours dies from overpopulation
    - Any live cell with 2~3 live neighbours lives
    - any dead cell with exactly 3 live neighbours comes to life

Cells:
    - 0 : Dead
    - 1 : Alive"""

from copy import deepcopy
from random import randint

class OldUniverse(object):
    def __init__(self, grid=None, steps=0):
        """ Intitialise the universe with the passed grid or an empty one """
        self.steps = steps
        if grid:
            self.grid = deepcopy(grid)
            self.width = len(grid)
            self.height = len(grid[0])
        else:
            self.generate_grid(40, 20)

    def generate_grid(self, width, height):
        """ Create an empty grid of size: width*height """
        self.width = width
        self.height = height
        self.grid = [[0 for row in range(height)] for column in range(width)]

    def __str__(self):
        """ String representation of the grid """
        string = ''.join(['-' for i in range(self.width)]) + '\n' # List comprehension to string
        for row in range(self.height):
            for column in range(self.width):
                cell = self.grid[column][row]
                if cell == 0:
                    string += ' '
                else:
                    string += '|'
            string += '\n'

        string += '\n' + ''.join(['-' for i in range(self.width)])
        return string

    def step(self):
        """ apply evolve() to every cell on the grid """
        updated = False
        game = self.__class__(self.grid, self.steps+1)
        
        for row in range(self.height):
            for column in range(self.width):
                live_neighbours = 0
                if row > 0:
                    live_neighbours += self.grid[column][row-1] # Check on top
                    if column > 0:
                        live_neighbours += self.grid[column-1][row-1] # Check top left
                    if column < self.width-1:
                        live_neighbours += self.grid[column+1][row-1] # Check top right
                if row < self.height-1:
                    live_neighbours += self.grid[column][row+1] # Check at bottom
                    if column > 0:
                        live_neighbours += self.grid[column-1][row+1] # Check bottom left
                    if column < self.width-1:
                        live_neighbours += self.grid[column+1][row+1] # Check bottom right
                if column > 0:
                    live_neighbours += self.grid[column-1][row] # Check left
                if column < self.width-1:
                    live_neighbours += self.grid[column+1][row] # Check right

                if game.evolve(column, row, live_neighbours):
                    updated = True

        self.grid = game.grid
        self.steps += 1
        return updated
                
    def evolve(self, column, row, live_neighbours):
        updated = False
        state = self.grid[column][row]
        #print(live_neighbours)
        if live_neighbours not in [2,3] and state != 0: # Exposure and overpopulation
            self.grid[column][row] = 0
            updated = True
        elif live_neighbours == 3 and state != 1:
            self.grid[column][row] = 1
            updated = True
        return updated
            

    def toggle_state(self, column, row):
        """ invert the state of a particular cell"""
        self.grid[column][row] = 1 - self.grid[column][row] # Change between 0-1 and 1-0

    def set_cell(self, column, row, state):
        """ set the state of a particular cell"""
        self.grid[column][row] = state

    def clear(self):
        self.grid = [[0 for row in range(self.height)] for column in range(self.width)]
        self.steps = 0

    def fill(self):
        self.grid = [[1 for row in range(self.height)] for column in range(self.width)]
        self.steps = 0

    def random(self):
        self.grid = [[randint(0, 1) for row in range(self.height)] for column in range(self.width)]
        self.steps = 0

    def invert(self):
        self.grid = [[1 - self.grid[column][row] for row in range(self.height)] for column in range(self.width)]
        self.steps = 0

if __name__ == '__main__':
    game = OldUniverse()
    game.random()
    print(game)

