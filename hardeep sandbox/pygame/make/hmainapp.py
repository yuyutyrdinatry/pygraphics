import wx
import wx.lib.newevent

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

if __name__ == '__main__':
     app = hMainApp()
     app.MainLoop()
