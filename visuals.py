import pygame, time
from constants import *

pygame.init()
pygame.display.init()

#create a screen
class Screen():
    def __init__(self):
        pygame.display.set_caption("CHIP8 Simulator by Meyan")
        self.screen = pygame.display.set_mode((64*RESOLUTION, 32*RESOLUTION))

        # filling the pixels: 32 rows (height), 64 cols (width)
        self.pixels = [[0 for i in range(64)] for j in range(32)]
        self.running = True # required for main screen loop
    
    def checkKeyPress(self,key):
        keys = pygame.key.get_pressed()
        if key == 1 and keys[pygame.K_KP1]:
            return True
        if key ==2 and keys[pygame.K_KP2]:
            return True
        if key ==3 and keys[pygame.K_KP3]:
            return True
        if key ==4 and keys[pygame.K_KP4]:
            return True
        if key ==5 and keys[pygame.K_KP5]:
            return True
        if key ==6 and keys[pygame.K_KP6]:
            return True
        if key ==7 and keys[pygame.K_KP7]:
            return True
        if key ==8 and keys[pygame.K_KP8]:
            return True
        if key ==9 and keys[pygame.K_KP9]:
            return True
        if key ==0xa and keys[pygame.K_a]:
            return True
        if key ==0xb and keys[pygame.K_b]:
            return True
        if key ==0xc and keys[pygame.K_c]:
            return True
        if key ==0xd and keys[pygame.K_d]:
            return True
        if key ==0xe and keys[pygame.K_e]:
            return True
        if key ==0xf and keys[pygame.K_f]:
            return True
    
    def clear_display(self):
        for i in range(64):
            for j in range(32):
                self.pixels[j][i] = 0
                pygame.draw.rect(self.screen, (0, 0, 0), (i*RESOLUTION, j*RESOLUTION, RESOLUTION, RESOLUTION))

    
    def toggle_pixel(self, x, y):
        x %= 64
        y %= 32



        if self.pixels[y][x] == 0:
            self.pixels[y][x] = 1
            pygame.draw.rect(self.screen, (255, 255, 255), (x*RESOLUTION, y*RESOLUTION, RESOLUTION, RESOLUTION))
        else:
            self.pixels[y][x] = 0
            pygame.draw.rect(self.screen, (0, 0, 0), (x*RESOLUTION, y*RESOLUTION, RESOLUTION, RESOLUTION))
            return True

        pygame.display.update()
    
    def draw_sprite(self, sprite, x, y):
        toReturnTrue = False
        current_x = x
        current_y = y

        for sps in sprite:
            toPlot = format(sps, "08b")
            for data in toPlot:
                if data == "1":
                    if self.toggle_pixel(current_x, current_y):
                        toReturnTrue = True
                current_x += 1
            current_y += 1
            current_x = x
        return toReturnTrue
    
    def wait_key_press(self):
        while True:
            for evs in pygame.event.get():
                if evs.type == pygame.QUIT:
                    self.running = False
                    return True

                if evs.type == pygame.KEYDOWN:
                    match evs.key:
                        case pygame.K_KP0:
                            return 0
                        case pygame.K_KP1:
                            return 1
                        case pygame.K_KP2:
                            return 2
                        case pygame.K_KP3:
                            return 3
                        case pygame.K_KP4:
                            return 4
                        case pygame.K_KP5:
                            return 5
                        case pygame.K_KP6:
                            return 6
                        case pygame.K_KP7:
                            return 7
                        case pygame.K_KP8:
                            return 8
                        case pygame.K_KP9:
                            return 9
                        case pygame.K_a:
                            return 0xa
                        case pygame.K_b:
                            return 0xb
                        case pygame.K_c:
                            return 0xc
                        case pygame.K_d:
                            return 0xd
                        case pygame.K_e:
                            return 0xe
                        case pygame.K_f:
                            return 0xf
                        case default:
                            return 1
 
        
    def mainloop(self):
        for evs in pygame.event.get():
            if evs.type == pygame.QUIT:
                self.running = False

        return self.running
