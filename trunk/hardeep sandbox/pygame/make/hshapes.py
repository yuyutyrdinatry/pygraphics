import pygame
import color

class hShape(object):
    def circle(self, radius, color):
        pass
    
    class rectangle(object):
        def __init__(self, w, h, color):
            self.w = w
            self.h = h
            
            if ( isinstance(color, color.Color) ):
                self.color = color.get_rgb()
            else:
                self.color = color
            
        def draw_at(self, surf, x, y):
            return pygame.draw.rect(surf, self.color, (x,y,w,h), width=0):