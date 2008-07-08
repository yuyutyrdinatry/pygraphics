import pygame
from hevents import *
from hconstants import *

import pymunk
from pymunk.vec2d import *
import math

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
        self.physics = False
        self.set_physics = False
        self.init_physics = False
        
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
            
    def do_init_phys(self, space):
        if self.set_physics:
            self.physics = True
            self.physical_space = space
            
            self.inertia = self.look.get_inertia()
            self.mass = self.look.get_mass()
            
            self.body = pymunk.Body(self.mass, self.inertia)
            self.body.position = self.pos[0], self.pos[1]
            
            self.physical_shape = self.look.get_shape(self.body)
            self.physical_space.add(self.body, self.physical_shape)
        
    def do_phys(self):
        pass
        
    def add_force(self, x, y):
        vect = (x, y)
        
    def draw(self, surf):
        if ( self.look is not None ):
            if ( self.physics ):
                self.pos = (self.body.position.x, self.body.position.y)
            self.look.draw_at(surf, self.pos[0], self.pos[1])
            
    def launch_events(self, e):
        if ( e.type != 0 ):
            for key in self.events:
                # Helper function needed here
                if ( e.type == key ):
                    self._launch_events(key, e)
                elif ( key == H_EVENT_FRAME_UPDATE ):
                    self._launch_events(key, e)
                elif ( key == H_EVENT_INIT_PHYSICS and not self.init_physics ):
                    self.init_physics = True
                    self._launch_events(key, e)
    
    def _launch_events(self, key, e):
        if ( len(self.events[key]) == 1 ):
            self.events[key][0](self, e)
        else:
            for func in self.events[key]:
                func(self, e)
        
    def add_event(self, e, f, overwrite=True):
        if ( overwrite is False ):
            if ( self.events.has_key(e) ):
                self.events[e].append(f)
            else:
                self.events[e] = [f]
        else:
            self.events[e] = [f]