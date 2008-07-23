# You know, I keep thinking it'd be really cool to have a very simple game-
# maker sort of class that could allow people to relatively easily put together
# simple games. Indeed. It would be quite cool.

# Notes:
# http://wiki.slembcke.net/main/published/Chipmunk
# http://www.pygame.org/project/780/
# http://code.google.com/p/pymunk/
# http://code.google.com/p/pymunk/wiki/SlideAndPinJointsExample
#
# What you will need:
# PyGame 1.8+ http://www.pygame.org/download.shtml
# PyMunk 0.8+ http://code.google.com/p/pymunk/
#             If PyMunk is not being installed on windows, MAKE SURE you compile
#             the Chipmunk library yourself for your own system! It works on
#             Mac + Linux, but you must compile it. Instructions are on the site

import os, sys
import wx
import threading
from pygame.locals import *

from hconstants import *
from hsdl import *
from hobj import *
from hshapes import *
from hevents import *
from hmainapp import *

import pymunk
from pymunk.vec2d import *
import math

import pygame

class hMain(hMainAppThread):
    def __init__(self, window_name="Frame", rate=50):
        hMainAppThread.__init__(self)
        self.window_name = window_name
        self.SDL_thread = None
        self.rate = rate
        self.start_physics = False
    
    def init_physics(self):
        pass
    
    def init_game(self):
        pass
        
    def set_physics_on(self):
        self._lock.acquire()
        self.SDL_thread.set_physics_on()
        self._lock.release()
        
    def set_gravity(self, x=0.0, y=-900.0):
        self._lock.acquire()
        self.SDL_thread.set_gravity(x, y)
        self._lock.release()
        
    def add_obj(self, o, z_order=0):
        self._lock.acquire()
        self.SDL_thread.add_obj(o, z_order)
        self._lock.release()
        
    def run(self):
        try:
            self.hmain = hMainApp()
            self.frame = SDLFrame(None, wx.ID_ANY, self.window_name, 
                                  (H_WIN_WIDTH, H_WIN_HEIGHT))
            self.frame.Show()
            
            # Convenience references
            self.SDL_thread = self.frame.thread
            self.pyg_screen = self.frame.panel.window
            
            self._lock.release()
            
            if self.start_physics:
                self.set_physics_on()
                self.set_gravity()
                self.init_physics()
            self.init_game()
            
            self.hmain.MainLoop()
        finally:
            # If an exception occurs, lets end the thread process....hopefully
            pass

if __name__ == '__main__':
    app = hMain('Test')
    app.start()
    
    app.add_wx_obj('blah', wx.Frame, True, None, -1, "Frame", pos=(50,50), size=(600,600))