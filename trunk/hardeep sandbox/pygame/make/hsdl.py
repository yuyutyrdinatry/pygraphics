# http://wiki.wxpython.org/IntegratingPyGame
import os, sys
import wx
import threading

import pymunk
from pymunk.vec2d import *
import math

global pygame

class SDLThread(threading.Thread):
    def __init__(self, screen, window, rate=50):
        threading.Thread.__init__(self)
        
        self.run_thread = False
        self.screen = screen
        self.window = window
        self.objects = {}
        self.objects_keys = []
        self.physics = False
        self.physical_space = None
        self.rate = rate
        
    def add_obj(self, o, z_order=0):
        if ( not self.objects.has_key(z_order) ):
            self.objects[z_order] = []

        o.do_init_phys(self.physical_space)
            
        self.objects[z_order].append(o)        
        self.objects_keys = self.objects.keys()
        self.objects_keys.sort()
        
    def set_physics_on(self):
        self.physics = True
        pymunk.init_pymunk()
        self.physical_space = pymunk.Space()
        
        # Set physical space for each object
        for key in self.objects_keys:
            for o in self.objects[key]:
                o.set_physical_space(self.physical_space)
    
    def set_gravity(self, x=0.0, y=-900.0):
        if ( self.physics ):
            self.physical_space.gravity = Vec2d(x, y)

    def run(self):
        self.run_thread = True
        
        # Local Vars for Speed
        clock_tick = pygame.time.Clock().tick
        main_loop = self._main_loop
        rate = self.rate
        
        while self.run_thread:
            main_loop(clock_tick, rate)

    def stop(self, e=None):
        self.run_thread = False
        if ( e is not None ):
            e.Skip()
        
    def _main_loop(self, clock_tick, rate):
        e = pygame.event.poll()
        
        if e.type == pygame.QUIT:
            self.stop()
            self.window.Destroy()
            return

        self.screen.fill((0,0,0)) # Black BG
        
        for key in self.objects_keys:
            for o in self.objects[key]:
                o.launch_events(e)
                o.draw(self.screen)
        
        if ( self.physics ):
            self.physical_space.step(1.0/rate)
            
        pygame.display.flip()
        clock_tick(rate)

class SDLPanel(wx.Panel):
    def __init__(self, parent, ID, window_size, rate=50):
        '''Init pygame display into the Frame as a Panel.'''
        global pygame
        
        wx.Panel.__init__(self, parent, ID, size=window_size)
        self.Fit()
        
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        
        # this has to happen AFTER setting the environment variables above.
        import pygame
        
        pygame.display.init()
        self.window = pygame.display.set_mode(window_size)
        
        self.parent = parent
        parent.thread = SDLThread(self.window, parent, rate)
        parent.thread.start()
        
        parent.Bind(wx.EVT_CLOSE, parent.thread.stop)

    def __del__(self):
        self.parent.stop()

class SDLFrame(wx.Frame):
    def __init__(self, parent, ID, window_title, window_size, rate=50):
        style = wx.SYSTEM_MENU|wx.CLOSE_BOX|wx.CAPTION|wx.MINIMIZE_BOX
        wx.Frame.__init__(self, parent, ID, window_title, size=window_size, 
                          style=style)
        self.panel = SDLPanel(self, -1, window_size, rate)