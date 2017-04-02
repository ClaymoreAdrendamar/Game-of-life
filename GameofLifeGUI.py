from GameofLife import universe
import pygame
from pygame.locals import *
import time
from copy import deepcopy

class GUI(object):
    def __init__(self):
        self.universe = universe()
        self.cell_size = 20
        
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400),RESIZABLE)
        pygame.display.set_caption('Conway\'s game of life')
        self.redraw = True
        self.end = False

        self.last_transform_time = self.last_time = time.time()
        self.speed = 0.1 # Time between each update in seconds

        self.pause = True
        self.old_grid = deepcopy(self.universe.grid)

        self.left = False
        self.right = False
        self.up = False
        self.down = False

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
            elif event.type == VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],RESIZABLE)
                self.redraw = True
                print('[+] Resized window')
                screen_width, screen_height = pygame.display.get_surface().get_size()
                print('Screen width: {}, height: {}'.format(screen_width, screen_height))
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and self.pause == True: # Left click and paused
                    print('[~] Left click')
                    x, y = event.pos
                    x = int(x/(self.cell_size+1))
                    y = int(y/(self.cell_size+1))
                    self.universe.toggle_state([x,y])
                    self.redraw = True
                    print('[+] Toggled cell at x: ',x,', y: ',y)
                elif event.button == 3: # If right click
                    print('[~] Right click')
                    self.pause = not self.pause # Pause
                    print('[+] Toggled pause state')
                elif event.button == 5: # If scroll down
                    print('[~] Scroll down')
                    self.speed += 0.1 # Slow down
                    print('[+] Slowed down')
                elif event.button == 4: # If scroll up
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
                elif event.key == pygame.K_n and self.pause == True: #Next step
                    print('[~] Pressed N')
                    self.update()
                    print('[+] Next step')
                elif event.key == pygame.K_LEFT:
                    print('[+] Pressed LEFT ARROW')
                    self.left = True
                elif event.key == pygame.K_RIGHT:
                    print('[+] Pressed RIGHT ARROW')
                    self.right = True
                elif event.key == pygame.K_UP:
                    print('[+] Pressed UP ARROW')
                    self.up = True
                elif event.key == pygame.K_DOWN:
                    print('[+] Pressed DOWN ARROW')
                    self.down = True
            elif event.type == KEYUP:
                if event.key == pygame.K_LEFT:
                    print('[+] Released LEFT ARROW')
                    self.left = False
                elif event.key == pygame.K_RIGHT:
                    print('[+] Released RIGHT ARROW')
                    self.right = False
                elif event.key == pygame.K_UP:
                    print('[+] Released UP ARROW')
                    self.up = False
                elif event.key == pygame.K_DOWN:
                    print('[+] Released DOWN ARROW')
                    self.down = False
        current_time = time.time()
        if current_time - self.last_transform_time >= 0.1:
            if self.left:
                self.universe.transform(1,0)
                self.redraw = True
            if self.right:
                self.universe.transform(-1,0)
                self.redraw = True
            if self.up:
                self.universe.transform(0,1)
                self.redraw = True
            if self.down:
                self.universe.transform(0,-1)
                self.redraw = True
            self.last_transform_time = current_time
                
    def update(self):
        """ Update environment """
        current_time = time.time()
        if current_time - self.last_time >= self.speed:
            #print('[~] Updating environment')
            self.last_time = current_time
            if self.universe.step():
                self.redraw = True
            else:
                self.pause = True
                print('[+] Activated pause state')
            #print('[+] Environment updated')

    def draw(self):
        """ Display the environment """
        # Fill the screen
        self.screen.fill((0,0,0))
        screen_width, screen_height = pygame.display.get_surface().get_size()
        width = int(screen_width / self.cell_size)
        height = int(screen_height / self.cell_size)
        # Draw universe
        for row in range(height):
            for column in range(width):
                x = column*self.cell_size+column
                y = row*self.cell_size+row
                if self.universe.belong([column, row]):
                    colour = (100,100,200)
                else:
                    colour = (150,150,150)
                pygame.draw.rect(self.screen, colour, (x,y,self.cell_size,self.cell_size), 0)
        pygame.display.update()
    

if __name__ == '__main__':
    gui = GUI()
    gui.loop()
