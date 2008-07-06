import pygame
from hevents import *
from hconstants import *

class hObj(object):
    
    def __init__(self, name, **kwargs):
        '''
        Keywords accepted:
        '''
        self.__init_vars()
        
        self.name = name
        self.events = {}
        
    def __init_vars(self):
        self.look = None
        self.pos = H_WIN_CENTER
        
    def set_pos(self, p):
        if p == -1:
            c = H_WIN_CENTER_COORDS
            w = self.look.w
            h = self.look.h
            x = c[0] - (w / 2)
            y = c[1] - (h / 2)
            
            self.pos = (x, y)
        else:
            self.pos = p
        
    def draw(self, surf):
        if ( self.look is not None ):
            self.look.draw_at(surf, self.pos[0], self.pos[1])
            
    def launch_events(self, e):
        if ( e.type != 0 ):
            for key in self.events:
                if ( e.type == key ):
                    if ( len(self.events[key]) == 1 ):
                        self.events[key][0](self, e)
                    else:
                        for func in self.events[type]:
                            func(self, e)
        
    def add_event(self, e, f, overwrite=True):
        if ( overwrite is False ):
            if ( self.events.has_key(e) ):
                self.events[e].append(f)
            else:
                self.events[e] = [f]
        else:
            self.events[e] = [f]