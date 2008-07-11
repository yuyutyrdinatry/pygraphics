import pygame
import color

import pymunk
from pymunk.vec2d import *
import math

class hShape(object):
    class base_shape(object):
        def __init__(self, w, h, c, width=0, mass_factor=0.1):
            self.set_size(w, h)
            self.set_color(c)
            self.set_width(width)
            self.set_mass_factor(mass_factor)
            
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
                
        def get_poly(self):
            # Needed for any object which is not a circle
            pass
                
        def get_inertia(self):
            pass
        
        def get_mass(self):
            pass
        
        def get_shape(self):
            pass
            
        def draw_at(self, surf, x, y):
            pass        
    
    class rectangle(base_shape):
        def get_poly(self):
            pass
        
        def get_inertia(self):
            return pymunk.moment_for_poly(self.get_mass(), self.get_poly(), Vec2d(0,0))
        
        def get_mass(self):
            return self.w * self.h * self.factor
        
        def get_shape(self):
            pass
        
        def draw_at(self, surf, x, y):
            return pygame.draw.rect(surf, self.color, (x,y,self.w,self.h), self.width)
        
    class circle(base_shape):
        def __init__(self, r, c, width=0, mass_factor=0.1):
            self.set_size(r)
            self.set_color(c)
            self.set_width(width)
            self.set_mass_factor(mass_factor)
            
        def set_size(self, r):
            hShape.base_shape.set_size(self, r, r)
            self.r = r
            
        def set_mass_factor(self, mass_factor):
            self.factor = mass_factor
            
        def draw_at(self, surf, x, y):
            return pygame.draw.circle(surf, self.color, (int(x), int(y)), self.r, self.width)
        
        def get_inertia(self):
            return pymunk.moment_for_circle(self.get_mass(), 0, self.r, Vec2d(0,0))
        
        def get_mass(self):
            # Note: make the mass a function of the surface area
            return math.pi * self.r * self.r * self.factor
        
        def get_shape(self, body):
            return pymunk.Circle(body, self.r, Vec2d(0,0))