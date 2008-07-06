# You know, I keep thinking it'd be really cool to have a very simple game-
# maker sort of class that could allow people to relatively easily put together
# simple games. Indeed. It would be quite cool.

# Notes:
# http://wiki.slembcke.net/main/published/Chipmunk

import os, sys
import wx
import threading
from pygame.locals import *
from hsdl import *

global pygame # when we import it, let's keep its proper name!

class hMain(threading.Thread):
    def __init__(self, window_name="Frame"):
        threading.Thread.__init__(self)
        self.window_name = window_name
        
    def run(self):
        self.app = hMainApp()
        self.frame = SDLFrame(None, wx.ID_ANY, self.window_name, (640,480))
        self.frame.Show()
        
        # Convenience references
        self.SDL_thread = self.frame.thread
        self.pyg_screen = self.frame.panel.window
        
        self.app.MainLoop()

class hMainApp(wx.PySimpleApp):
    def __init__(self):
        wx.PySimpleApp.__init__(self)

if __name__ == '__main__':
    app = hMain('Test')
    app.start()
    
    # This is what I want the above code to eventually look like. In less than
    # 10 lines of code, recreate the above!
    # --------------------------------------------------------------------------
    ## app = hMain('Test')
    ## app.start()
    ## 
    ## def move_obj(self, event):
    ##     event.obj.movie(event.mouse.x, event.mouse.y)
    ## 
    ## obj = hObj('rectangle')
    ## obj.look = hShape.rectangle(100,100) #shape, picture, PIL, movie, w/elif
    ## obj.initial_pos = (0,0)
    ## obj.add_event('on_click', move_obj)
    ## 
    ## app.add_obj(obj)
    # --------------------------------------------------------------------------
    # Now THAT would be sick
    #
    # What about a more complex example? A While ago I made a Gravity game...
    # Perhaps a simple recreation of that (one level, two planets, one asteroid)
    # could look like this?
    #
    from hmake import *
    import random
    
    class Gravity(hMain):
        
        class Planet(hObj):
            def __init__(self):
                hObj.__init__('Circle')
                self.look = hShape.circle(random.randint(50,200), (255,255,255))
                self.inital_pos = H_CENTER
                self.add_event('draw_frame', self.event_draw_frame)
                
            def event_draw_frame(self, event):
                '''Executes on every drawn frame.'''
                objs = event.objs
        
        def __init__(self):
            hMain.__init__(self, 'Gravity')
            self._make_and_add_planet()
            
        def _make_and_add_planets(self):
            self.add_obj(Planet())
            self.add_obj(Planet())