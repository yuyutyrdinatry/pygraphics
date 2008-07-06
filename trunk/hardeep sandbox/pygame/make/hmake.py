# You know, I keep thinking it'd be really cool to have a very simple game-
# maker sort of class that could allow people to relatively easily put together
# simple games. Indeed. It would be quite cool.

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
        self.SDL_thread = self.frame.thread
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