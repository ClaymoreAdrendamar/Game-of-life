from OldGameofLife import OldUniverse
import pygame
from pygame.locals import *
import time
from copy import deepcopy

class environment(object):
    def __init__(self):
        self.universe = OldUniverse()
        width = int(input("Grid width: "))
        height = int(input("Grid height: "))
        self.cell_size = int(input("Cell size: "))
        self.universe.generate_grid(width,height)
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.universe.width*(self.cell_size+1)-1, self.universe.height*(self.cell_size+1)-1))
        pygame.display.set_caption('Conway\'s game of life Step: {}'.format(self.universe.steps))
        self.redraw = True
        self.end = False

        self.last_time = time.time()
        self.speed = 0.0 # Time between each update in seconds

        self.pause = True
        self.old_grid = deepcopy(self.universe.grid)

    def loop(self):
        """ Screen loop """
        print('[+] Beginning loop')
        while not self.end:
            self.process_inputs()
            if not self.pause:
                self.update()
            if self.redraw:
                self.draw()
                self.redraw = False
        print('[-] Loop ended')
        pygame.quit()

    def process_inputs(self):
        """ Process all user inputs """
        for event in pygame.event.get():
            #print('[~] Processing inputs')
            if event.type == QUIT:
                print('[-] Ending loop')
                self.end = True
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and self.pause == True: # Left click and paused
                    print('[~] Left click')
                    x, y = event.pos
                    x = int(x/(self.cell_size+1))
                    y = int(y/(self.cell_size+1))
                    self.universe.toggle_state(x,y)
                    self.redraw = True
                    print('[+] Toggled cell at x: ',x,', y: ',y)
                elif event.button == 3: # Right click
                    print('[~] Right click')
                    self.pause = not self.pause
                    print('[+] Toggled pause state')
                elif event.button == 5: # Scroll down
                    print('[~] Scroll down')
                    self.speed += 0.1 # Slow down
                    print('[+] Slowed down')
                elif event.button == 4: # Scroll up
                    print('[~] Scroll down')
                    self.speed -= 0.1 # Speed up
                    if self.speed < 0:
                        self.speed = 0
                    print('[+] Speeded up')
            elif event.type == KEYDOWN:
                if event.key == pygame.K_c and self.pause == True:#Clear
                    print('[~] Pressed C')
                    self.universe.clear()
                    print('[+] Cleared universe')
                    self.redraw = True
                elif event.key == pygame.K_f and self.pause == True: #Fill
                    print('[~] Pressed F')
                    self.universe.fill()
                    print('[+] Filled universe')
                    self.redraw = True
                elif event.key == pygame.K_n and self.pause == True: #Next step
                    print('[~] Pressed N')
                    self.update()
                    print('[+] Next step')
                elif event.key == pygame.K_r and self.pause == True: #Random
                    print('[~] Pressed R')
                    self.universe.random()
                    self.redraw = True
                    print('[+] Randomised grid')
                elif event.key == pygame.K_i and self.pause == True: #Invert
                    print('[~] Pressed I')
                    self.universe.invert()
                    self.redraw = True
                    print('[+] Inverted grid')
                
    def update(self):
        """ Update environment """
        current_time = time.time()
        if current_time - self.last_time >= self.speed:
            #print('[~] Updating environment')
            self.last_time = current_time
            if self.universe.step():
                pygame.display.set_caption('Conway\'s game of life Step: {}'.format(self.universe.steps))
                self.redraw = True
                
            if self.universe.grid == self.old_grid: # Check if the grid is at a standstill
                print('[+] Paused state: universe is stable')
                self.pause = True
            self.old_grid = self.universe.grid
            #print('[+] Environment updated')

    def draw(self):
        """ Display the environment """
        #print('[~] Updating screen')
        # Fill the screen
        self.screen.fill((0,0,0))
        # Draw universe
        for row in range(self.universe.height):
            for column in range(self.universe.width):
                x = column*self.cell_size+column
                y = row*self.cell_size+row
                if not row and not column:
                    print('X: {}, Y: {}'.format(x,y))
                if self.universe.grid[column][row] == 0:
                    colour = (150,150,150)
                elif self.universe.grid[column][row] == 1:
                    colour = (100,100,200)
                pygame.draw.rect(self.screen, colour, (x,y,self.cell_size,self.cell_size), 0)
        pygame.display.update()
        #print('[+] Screen updated')
    

if __name__ == '__main__':
    environment = environment()
    environment.loop()
