import threading
try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required."

class ShowWrapperThread(threading.Thread):
    '''Wraps wxShow's MainLoop into it's own thread.'''
    
    def __init__(self):
        threading.Thread.__init__(self, None, self.run, "wxShow")
        self.setDaemon(1)
        self.app = wx.App()
        self.frame = wxShow(None,-1,'my threaded window')
        
    def run(self):
        self.app.MainLoop()

class wxShow(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title)
        self.parent = parent
        self.__init_window()

    def __init_window(self):
        self.Show(True)
        
if __name__ == "__main__":
    a = ShowWrapperThread()
    a.start()