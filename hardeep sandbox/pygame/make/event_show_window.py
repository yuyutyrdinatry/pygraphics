# Fully event based wx window...the frames and all objects are created via
# events and the drawing is also handled as an event.

import threading
import wx
import wx.lib.dragscroller
import time
from hmainapp import *

EVT_NEW_IMAGE = wx.PyEventBinder(wx.NewEventType(), 0)

class ImageEvent(wx.PyCommandEvent):
    def __init__(self, eventType=EVT_NEW_IMAGE.evtType[0], id=0):
        wx.PyCommandEvent.__init__(self, eventType, id)
        self.pic = None
        self.event_lock = None

class ShowWindow(object):
    def __init__(self):
        self.frame = None
        self.iWindow = None
        self.pic = None
        self._lock = threading.Lock()
        
        self._lock.acquire()
        self.app = hMainAppThread('Show Window')
        self.app.start()
        
        print '-------- Frame'
        self.app.add_wx_obj('Frame', wx.Frame, True, None)
        print '-------- iWindow'
        self.frame = self.app.get_obj('Frame')
        self.app.add_wx_obj('iWindow', ImageWindow, False, self.frame)
        self.iWindow = self.app.get_obj('iWindow')
        self._lock.release()

    def load_image(self, pic):
        self._lock.acquire()
        self.frame.SetSize((pic.get_width(), pic.get_height()))
        self.frame.SetTitle('File: ' + pic.get_filename())
        self.pic = pic
        self.iWindow.load_image(self.pic)
        self.frame.Refresh()
        self._lock.release()
        
    def refresh(self):
        self._lock.acquire()
        #self.iWindow.load_image(self.pic)
        self.frame.Refresh()
        self._lock.release()        
        
class ImageWindow(wx.ScrolledWindow):
    def __init__(self, parent=None, id=-1):
        self.parent = parent
        style = wx.FULL_REPAINT_ON_RESIZE|wx.ALWAYS_SHOW_SB|wx.CLIP_CHILDREN
        wx.ScrolledWindow.__init__(self, parent, id, style=style)
        self._set_binds()
        self._init_scroll()        
        self.pic = None
        self.xy = [0, 0]
        
        self.pic_copy = None
        self._lock = threading.Lock()
        
    def load_image(self, pic):
        self.pic = pic
        self._launch_draw_event()
        
    #===========================================================================
    # Helper Methods
    #===========================================================================
    def _get_DC(self):
        dc = wx.PaintDC(self)
        self.DoPrepareDC(dc)
        return dc
    
    def _launch_draw_event(self):
        #Create the event
        event = ImageEvent()
        event.pic = self.pic
        event.event_lock = self._lock
        
        print 'event created', event
        #Trigger the event when app releases the eventLock
        event.event_lock.acquire() #wait until the event lock is released
        self.AddPendingEvent(event)
    
    def _update_display(self, dc):
        w, h = self.GetSize()
        dc.SetBackgroundMode(wx.TRANSPARENT)
        if ( self.pic is not None ):
            bmp = _convert_picture_to_bitmap(self.pic)
            xy = [bmp.GetWidth(), bmp.GetHeight()]
            
            pos_x = max((w - xy[0]) / 2, 0)
            pos_y = max((h - xy[1]) / 2, 0)
            
            dc.DrawBitmap(bmp, pos_x, pos_y, False)
            if ( self.xy != xy ):
                self.xy = xy
                self.SetScrollbars(1, 1, xy[0], xy[1], 0, 0)
                
    def _set_binds(self):
        self.Bind(wx.EVT_PAINT, self.event_paint)
        self.Bind(wx.EVT_RIGHT_DOWN, self.event_right_down)
        self.Bind(wx.EVT_RIGHT_UP, self.event_right_up)
        self.Bind(EVT_NEW_IMAGE, self.event_new_image)
        
    def _init_scroll(self):
        self.SetScrollbars(1, 1, 10, 10, 0, 0)
        self.scroller = wx.lib.dragscroller.DragScroller(self)
        self.scroller.SetSensitivity(self.scroller.GetSensitivity() / 2)
        
    #===========================================================================
    # Event Handlers
    #===========================================================================
    def event_paint(self, event):
        self._update_display(self._get_DC())
        
    def event_right_down(self, event):
        self.scroller.Start(event.GetPosition())

    def event_right_up(self, event):
        self.scroller.Stop()
        
    def event_new_image(self, event):
        print 'new image event process', event
        self.pic = event.pic
        self._update_display(self._get_DC())
        print 'updated display'
        event.event_lock.release()
        print 'lock released'
        
def _convert_picture_to_bitmap(pic):
    if ( pic is not None ):
        pilImage = pic.get_image()
        image = _pil_to_image(pilImage)
        return wx.BitmapFromImage(image)
        
def _pil_to_image(pil, alpha=True):
    '''Convert PIL Image to wx.Image and return the result.'''
    
    if alpha:
        image = apply( wx.EmptyImage, pil.size )
        image.SetData( pil.convert( "RGB").tostring() )
        image.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
        
    else:
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        new_image = pil.convert('RGB')
        data = new_image.tostring()
        image.SetData(data)
        
    return image

if __name__ == '__main__':
    import picture
    import media
    
    a = ShowWindow()
    #a.start()
#    
    b = picture.Picture(400,200,picture.white)
    c = picture.Picture(500,500,picture.red)
#    # d = m.load_picture('test.png')
#    
    a.load_image(c)