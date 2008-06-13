import threading
try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

class ShowWrapperThread(threading.Thread):
    '''Wraps wxShow into it's own thread.'''
    
    def __init__(self):
        threading.Thread.__init__(self, None, self.run, "wxShow")
        self.setDaemon(1)
    
    def set_loop_bind(self, bind):
        self.bind = bind
        
    def run(self):
        '''Runs when the thread is started. Executes the local function bind.'''
        self.bind()
        
class ShowTimerThread(threading.Thread):
    '''Timer thread to update the show window.'''
    stop = False
        
    def run(self):
        '''Runs when the thread is started.'''
        
        # Create local variables of all functions, variables, etc... for speed
        get_time = time
        poll_interval = self.poll_interval
        update = self.update_bind
        
        a = get_time()
        while ( not self.stop ):
            delta_t = get_time() - a 
            if ( delta_t >= poll_interval ):
                a = get_time()
                update()
                
    def set_update_bind(self, bind):
        self.update_bind = bind
    
    def set_poll_interval(self, interval=1):
        '''Set the local poll_interval to the int interval which is the interval
        in which to update the canvas in seconds.'''
        self.poll_interval = interval
    
    def end(self):
        '''Set the local boolean self.stop to True.'''
        self.stop = True

class wxShow(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title)
        self.parent = parent
        self.__init_window()

    def __init_window(self):
        self.Show(True)
        
if __name__ == "__main__":
    app = wx.App()
    frame = wxShow(None,-1,'my threaded application')
    
    a = ShowWrapperThread()
    a.set_loop_bind(app.MainLoop)
    a.start()