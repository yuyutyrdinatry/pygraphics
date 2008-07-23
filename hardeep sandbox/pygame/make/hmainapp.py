import wx
import wx.lib.newevent
import threading

global OBJ_CREATE
global EVT_OBJECT_CREATE

OBJ_CREATE, EVT_OBJECT_CREATE = wx.lib.newevent.NewEvent()

class hMainApp(wx.PySimpleApp):
    def __init__(self):
        wx.PySimpleApp.__init__(self)
        
        self.objs = {}
        self.event_frame = wx.Frame(None, pos=(-10,-10), size=(0,0))
        self.event_frame.Show(False)
        self.event_frame.Bind(EVT_OBJECT_CREATE, self.event_create_obj)
        
    def event_create_obj(self, e):
        self.objs[e.name] = e.obj(*e.args, **e.kwargs)
        if e.show:
            self.objs[e.name].Show(True)

    def make_obj(self, name, obj, show=True, *args, **kwargs):
        e = OBJ_CREATE(name=name, obj=obj, show=show, args=args, kwargs=kwargs)
        wx.PostEvent(self.event_frame, e)
        
class hMainAppThread(threading.Thread):
    def __init__(self, window_name="Frame", rate=50):
        threading.Thread.__init__(self)
        self.hmain = None       
        self._lock = threading.Lock()
        self._lock.acquire()
        
    def add_wx_obj(self, name, obj, show, *args, **kwargs):
        self._lock.acquire()
        self.hmain.make_obj(name, obj, show, *args, **kwargs)
        self._lock.release()
        
    def run(self):
        try:
            self.hmain = hMainApp()            
            self._lock.release()
            self.hmain.MainLoop()
        finally:
            # If an exception occurs, lets end the thread process....hopefully
            pass

if __name__ == '__main__':
    app = hMainAppThread('Test')
    app.start()
    
    app.add_wx_obj('blah', wx.Frame, True, None, -1, "Event-created Frame", pos=(50,50), size=(600,600))
