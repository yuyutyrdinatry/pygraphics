# Diving back into the world of wx... yay :o

import threading
import wx
import os
import time

# Let's attempt to get this working in a style similar to pyglet...
class wxShowOMatic(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def _create_and_init_window(self):
        self.app = wx.App()

if __name__ == '__main__':
    import wx.lib as wxLib
    import wx.lib.floatcanvas.NavCanvas as wxNC
    a = wx.App()
    
    frame = wx.Frame(None, -1, 'title', (0,0), (400,400), wx.DEFAULT_FRAME_STYLE, 'name')
    panel = wxNC.NavCanvas(frame, -1, (100,100))
    frame.Show(True)
    frame.CenterOnScreen()
    
    a.MainLoop()
    
    #dlg.ShowModal()
    #dlg.Destroy()
    #dlg = ID(None, 'C:')
    #dlg.ShowModal()
    #dlg.Destroy()