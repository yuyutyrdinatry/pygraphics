import pygame
import color

class hShape(object):
    def circle(self, radius, color):
        pass
    
    class rectangle(object):
        def __init__(self, w, h, c):
            self.set_size(w, h)
            self.set_color(c)
            
        def set_size(self, w, h):
            self.w = w
            self.h = h
        
        def set_color(self, c):
            if ( isinstance(c, color.Color) ):
                self.color = c.get_rgb()
            else:
                self.color = c
            
        def draw_at(self, surf, x, y):
            return pygame.draw.rect(surf, self.color, (x,y,self.w,self.h), 0)