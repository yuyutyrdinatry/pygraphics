import pygame
import color

class hShape(object):
    class base_shape(object):
        def __init__(self, w, h, c, width=0):
            self.set_size(w, h)
            self.set_color(c)
            self.set_width(width)
            
        def set_size(self, w, h):
            self.w = w
            self.h = h
            
        def set_width(self, w):
            self.width = w
        
        def set_color(self, c):
            if ( isinstance(c, color.Color) ):
                self.color = c.get_rgb()
            else:
                self.color = c
            
        def draw_at(self, surf, x, y):
            return pygame.draw.rect(surf, self.color, (x,y,self.w,self.h), self.width)        
    
    class rectangle(base_shape):
        pass
        
    class circle(base_shape):
        def __init__(self, r, c, width=0):
            self.set_size(r)
            self.set_color(c)
            self.set_width(width)
            
        def set_size(self, r):
            hShape.base_shape.set_size(self, r, r)
            self.r = r
            
        def draw_at(self, surf, x, y):
            return pygame.draw.circle(surf, self.color, (x, y), self.r, self.width)