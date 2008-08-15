import wx
import wx.lib.newevent
import threading

global OBJ_CREATE
global EVT_OBJECT_CREATE
global LOCK
LOCK = threading.Lock()

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
        
        if len(self.objs) == 1:
            self.objs[e.name].Bind(wx.EVT_CLOSE, self.event_close)
        
        if e.show:
            self.objs[e.name].Show(True)
        LOCK.release()

    def make_obj(self, name, obj, show=True, *args, **kwargs):
        e = OBJ_CREATE(name=name, obj=obj, show=show, args=args, kwargs=kwargs)
        wx.PostEvent(self.event_frame, e)
        
    def event_close(self, e):
        self.event_frame.Destroy()
        e.Skip()
        
class hMainAppThread(threading.Thread):
    def __init__(self, window_name="Frame", rate=50):
        threading.Thread.__init__(self)
        self.hmain = None
        LOCK.acquire()
        
    def add_wx_obj(self, name, obj, show, *args, **kwargs):
        LOCK.acquire()
        self.hmain.make_obj(name, obj, show, *args, **kwargs)
        
    def get_obj(self, name):
        if self.hmain.objs.has_key(name):
            return self.hmain.objs[name]
        else:
            while not self.hmain.objs.has_key(name):
                True
            return self.get_obj(name)
        
    def run(self):
        try:
            self.hmain = hMainApp()            
            LOCK.release()
            self.hmain.MainLoop()
        except Exception:
            # If an exception occurs, lets end the thread process....hopefully
            return None

if __name__ == '__main__':
    app = hMainAppThread('Test')
    app.start()
    
    app.add_wx_obj('blah', wx.Frame, True, None, -1, "Event-created Frame", pos=(50,50), size=(600,600))
    
    if 1:
        DO_BIND = True
        
        # Trying this procedurally...
        import picture as p
        from event_show_window import convert_picture_to_bitmap
        import wx.lib.dragscroller
        
        frame = app.get_obj('blah')
        app.add_wx_obj('scroller', wx.ScrolledWindow, True, frame)
        scroller = app.get_obj('scroller')
        
        w = 200
        h = 200
        frame.SetSize((w, h))
        scroller.SetScrollbars(1, 1, w, h, 0, 0)

        pic = p.Picture(filename='test.jpg')
        
        def make_dc():
            dc = wx.PaintDC(scroller)
            scroller.DoPrepareDC(dc)
            return dc
        
        X_Y = [0, 0]
        
        def draw(event=None):
            global scroller
            global frame
            global pic
            global X_Y
            
            dc = make_dc()
            
            w, h = frame.GetSize()
            dc.SetBackgroundMode(wx.TRANSPARENT)
            
            bmp = convert_picture_to_bitmap(pic)
            xy = [bmp.GetWidth(), bmp.GetHeight()]
            
            pos_x = max((w - xy[0]) / 2, 0)
            pos_y = max((h - xy[1]) / 2, 0)
            
            dc.DrawBitmap(bmp, pos_x, pos_y, False)
            if ( X_Y != xy ):
                X_Y = xy
                scroller.SetScrollbars(1, 1, xy[0], xy[1], 0, 0)
        
        if DO_BIND:
            scroller.Bind(wx.EVT_PAINT, draw)
        else:
            draw()