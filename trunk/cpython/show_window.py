import threading
import wx
import wx.lib.dragscroller
import time

class ShowWindow(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.iWindow = None
        self.pic = None
        
    def load_image(self, pic):
        while ( self.iWindow is None ):
            True
        self.iWindow.load_image(pic)
        
        self.frame.SetSize((pic.get_width(), pic.get_height()))
        self.frame.SetTitle('File: ' + pic.get_filename())
        self.frame.Refresh()
        
    def run(self):
        self.app = wx.App()
        
        self.frame = wx.Frame(None)
        self.iWindow = ImageWindow(self.frame)
        self.frame.Show()
        
        self.app.MainLoop()
        
class ImagePoller(threading.Thread):
    def __init__(self, frame, poll):
        threading.Thread.__init__(self)
        self.frame = frame
        self.poll = max(poll, 1)
        
    def run(self):
        poll = self.poll
        frame = self.frame
        refresh = self.frame.Refresh
        sleep = time.sleep
        
        while ( True ):
            if ( frame is not None ):
                try:
                    refresh()
                    sleep(poll)
                except:
                    # Block threading-related exceptions from showing
                    pass
        
class ImageWindow(wx.ScrolledWindow):
    def __init__(self, parent=None, id=-1):
        self.parent = parent
        wx.ScrolledWindow.__init__(self, parent, id, 
                                   style=wx.FULL_REPAINT_ON_RESIZE|wx.ALWAYS_SHOW_SB|wx.CLIP_CHILDREN)
        self._set_binds()
        self._init_scroll()        
        self.pic = None
        self.xy = [0, 0]
        
        self.pic_copy = None
        
    def load_image(self, pic):
        self.pic = pic
        self._update_display(wx.ClientDC(self))
        
    #===========================================================================
    # Helper Methods
    #===========================================================================
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
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        
    def _init_scroll(self):
        self.SetScrollbars(1, 1, 10, 10, 0, 0)
        self.scroller = wx.lib.dragscroller.DragScroller(self)
        self.scroller.SetSensitivity(self.scroller.GetSensitivity() / 2)
        
    #===========================================================================
    # Event Handlers
    #===========================================================================
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.DoPrepareDC(dc)
        self._update_display(dc)
        
    def OnRightDown(self, event):
        self.scroller.Start(event.GetPosition())

    def OnRightUp(self, event):
        self.scroller.Stop()
        
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
    import media as m
    
    a = ShowWindow()
    a.start()
    
    b = picture.Picture(400,200,picture.white)
    c = picture.Picture(500,500,picture.red)
    d = m.load_picture('test.png')
    
    a.load_image(b)