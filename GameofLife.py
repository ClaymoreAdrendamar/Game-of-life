from copy import deepcopy

class universe():
    """ A new optimised universe """
    def __init__(self, grid=None):
        if grid:
            self.grid = deepcopy(grid)
        else:
            self.clear()
        
    def clear(self):
        self.grid = []
        
    def step(self):
        game = self.__class__(self.grid)
        
        for cell in self.grid:
            # Reproduce
            for t_cell in self.neighbours(cell):
                if self.live_neighbours(t_cell) == 3:
                    game.set_cell(t_cell, True)
            # Kill the overpoplated or underpopulated cells
            if self.live_neighbours(cell) not in [2,3]:
                game.set_cell(cell, False)

            

        if self.__dict__ != game.__dict__:
            self.__dict__ = game.__dict__
            return True
        else:
            return False
        

    def live_neighbours(self, cell):
        live_neighbours = 0
        for t_cell in self.neighbours(cell):
            #print("Considering cell's neighbour: {}".format(t_cell))
            if t_cell in self.grid:
                #print("Cell {} is Active".format(t_cell))
                live_neighbours += 1

        return live_neighbours

    def neighbours(self, cell):
        return [[x+cell[0], y+cell[1]] for x in range(-1,2) for y in range(-1,2) if x or y ]

    def set_cell(self, cell, state):
        try:
            index = self.grid.index(cell) #Get the index of the cell if it exists
            # Else, it throws a ValueError
            if not state: # If state is false
                del self.grid[index] # Delete the cell
        except ValueError: # The cell doesn't exist
            if state: # If state is True
                self.grid.append(cell) # Create the cell

    def belong(self, cell):
        if cell in self.grid:
            return True
        else:
            return False

    def toggle_state(self, cell):
        if self.belong(cell):
            self.set_cell(cell, False)
        else:
            self.set_cell(cell, True)

    def transform(self, x, y):
        for cell in self.grid:
            cell[0] += x
            cell[1] += y

    def __str__(self):
        if self.grid != []:
            min_y = min(cell[1] for cell in self.grid)
            min_x = min(cell[0] for cell in self.grid)

            y_coef = -1*min_y
            x_coef = -1*min_x
            
            width = max(cell[0] for cell in self.grid)+x_coef + 1
            height = max(cell[1] for cell in self.grid)+y_coef + 1
            print('Height: {}, Width: {}'.format(height, width))
            
            grid = [[x+x_coef,y+y_coef] for x,y in self.grid]
            
            string = '\n'
            div = ''.join(['-' for i in range(width)]) + '\n'
            string += div
            for row in range(height):
                for column in range(width):
                    if self.belong([column-x_coef, row-y_coef]):
                        string += 'X'
                    else:
                        string += ' '
                string += '\n'
            string += div
        else:
            string = '\n-----\nEMPTY\n-----\n'
        return string
    
if __name__=='__main__':
    import UniverseTest
            
                

            
            
