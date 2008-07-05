# Diving back into the world of wx... yay :o

import threading
import wx
import wx.lib.dragscroller

# Let's attempt to get this working in a style similar to pyglet...
class ShowWindow(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.iWindow = None
        
    def load_image(self, pic):
        while ( self.iWindow is None ):
            True
        self.iWindow.load_image(pic)
        
    def run(self):
        self.app = wx.PySimpleApp()
        self.frame = wx.Frame(None)
        self.iWindow = ImageWindow(self.frame)
        self.frame.Show()
        self.app.MainLoop()
        
class ImageWindow(wx.ScrolledWindow):
    def __init__(self, parent=None, id=-1):
        wx.ScrolledWindow.__init__(self, parent, id)
        self._set_binds()
        self._init_scroll()        
        self.pic = None
        self.xy = [0, 0]
        
    def load_image(self, pic):
       self.pic = pic
       # Need to find out how to force an update...
       #self._update_display(self._get_dc())
    
    def _update_display(self, dc):
        if ( self.pic is not None ):
            bmp = _convert_picture_to_bitmap(self.pic)
            xy = [bmp.GetWidth(), bmp.GetHeight()]
            w, y = self.GetSize()
            
            dc.DrawBitmap(bmp, 20, 0, False)
            if ( self.xy != xy ):
                self.xy = xy
                self.SetScrollbars(1, 1, xy[0], xy[1], 0, 0)
                self.SetSize((xy[0], xy[1]))
                
    def _set_binds(self):
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        
    def _init_scroll(self):
        self.SetScrollbars(1, 1, 10, 10, 0, 0)
        self.scroller = wx.lib.dragscroller.DragScroller(self)
        
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

import picture

a = ShowWindow()
a.start()

b = picture.Picture(400,200,picture.black)
a.load_image(b)