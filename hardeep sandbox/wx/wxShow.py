try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

class wxShow(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title)
        self.parent = parent
        self.__init_window()

    def __init_window(self):
        self.Show(True)
        
if __name__ == "__main__":
    app = wx.App()
    frame = wxShow(None,-1,'my application')
    
    import threading
    t = threading.Thread(None, app.MainLoop, "Show")
    t.setDaemon(1)
    t.start() 