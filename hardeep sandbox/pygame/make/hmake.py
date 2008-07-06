# You know, I keep thinking it'd be really cool to have a very simple game-
# maker sort of class that could allow people to relatively easily put together
# simple games. Indeed. It would be quite cool.

# Notes:
# http://wiki.slembcke.net/main/published/Chipmunk
# http://www.pygame.org/project/780/
# http://code.google.com/p/pymunk/
# http://code.google.com/p/pymunk/wiki/SlideAndPinJointsExample

import os, sys
import wx
import threading
from pygame.locals import *

from hconstants import *
from hsdl import *
from hobj import *
from hshapes import *
from hevents import *

import pygame

class hMain(threading.Thread):
    def __init__(self, window_name="Frame"):
        threading.Thread.__init__(self)
        self.window_name = window_name
        self.SDL_thread = None
        
    def add_obj(self, o):
        
        # Wait until the thread is created
        while ( self.SDL_thread is None ):
            True
            
        self.SDL_thread.add_obj(o)
        # Register Events Here
        
    def run(self):
        self.app = hMainApp()
        self.frame = SDLFrame(None, wx.ID_ANY, self.window_name, (H_WIN_WIDTH, 
                                                                  H_WIN_HEIGHT))
        self.frame.Show()
        
        # Convenience references
        self.SDL_thread = self.frame.thread
        self.pyg_screen = self.frame.panel.window
        
        self.app.MainLoop()

class hMainApp(wx.PySimpleApp):
    def __init__(self):
        wx.PySimpleApp.__init__(self)

if __name__ == '__main__':
#    app = hMain('Test')
#    app.start()
    print H_WIN_CENTER