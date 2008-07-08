# http://wiki.wxpython.org/IntegratingPyGame
import os, sys
import wx
import threading

global pygame

class SDLThread(threading.Thread):
    def __init__(self, screen):
        threading.Thread.__init__(self)
        
        self.run_thread = False
        self.screen = screen
        
        self.objects = []
        
    def add_obj(self, o):
        self.objects.append(o)

    def run(self):
        self.run_thread = True
        while self.run_thread:
            self._main_loop()

    def stop(self, e=None):
        self.run_thread = False
        if ( e is not None ):
            e.Skip()
        
    def _main_loop(self):
        e = pygame.event.poll()
        
        if e.type == pygame.QUIT:
            self.stop()
            return

        self.screen.fill((0,0,0))
            
        for o in self.objects:
            o.launch_events(e)
            o.draw(self.screen)
        
        pygame.display.flip()

class SDLPanel(wx.Panel):
    def __init__(self, parent, ID, window_size):
        '''Init pygame display into the Frame as a Panel.'''
        global pygame
        
        wx.Panel.__init__(self, parent, ID, size=window_size)
        self.Fit()
        
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        
        # this has to happen after setting the environment variables.
        import pygame
        
        pygame.display.init()
        self.window = pygame.display.set_mode(window_size)
        
        self.parent = parent
        parent.thread = SDLThread(self.window)
        parent.thread.start()
        
        parent.Bind(wx.EVT_CLOSE, parent.thread.stop)

    def __del__(self):
        self.parent.stop()

class SDLFrame(wx.Frame):
    def __init__(self, parent, ID, window_title, window_size):
        style = wx.SYSTEM_MENU|wx.CLOSE_BOX|wx.CAPTION|wx.MINIMIZE_BOX
        wx.Frame.__init__(self, parent, ID, window_title, size=window_size, 
                          style=style)
        self.panel = SDLPanel(self, -1, window_size)