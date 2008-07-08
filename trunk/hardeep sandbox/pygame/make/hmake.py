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

import pymunk
from pymunk.vec2d import *
import math

import pygame

class hMain(threading.Thread):
    def __init__(self, window_name="Frame", rate=50):
        threading.Thread.__init__(self)
        self.window_name = window_name
        self.SDL_thread = None
        self.rate = rate
        self.start_physics = False
        
    def _wait_for_SDL_thread(self):
        # Wait until the thread is created
        while ( self.SDL_thread is None ):
            True
    
    def init_physics(self):
        pass
        
    def set_physics_on(self):
        self._wait_for_SDL_thread()
        self.SDL_thread.set_physics_on()
        
    def set_gravity(self, x=0.0, y=-900.0):
        self._wait_for_SDL_thread()
        self.SDL_thread.set_gravity(x, y)
        
    def add_obj(self, o, z_order=0):
        self._wait_for_SDL_thread()
        self.SDL_thread.add_obj(o, z_order)
        
    def run(self):
        self.app = hMainApp()
        self.frame = SDLFrame(None, wx.ID_ANY, self.window_name, (H_WIN_WIDTH, 
                                                                  H_WIN_HEIGHT))
        self.frame.Show()
        
        # Convenience references
        self.SDL_thread = self.frame.thread
        self.pyg_screen = self.frame.panel.window
        
        if ( self.start_physics ):
            self.set_physics_on()
            self.set_gravity()
            self.init_physics()
        
        self.app.MainLoop()

class hMainApp(wx.PySimpleApp):
    def __init__(self):
        wx.PySimpleApp.__init__(self)

if __name__ == '__main__':
    app = hMain('Test')
    app.start()