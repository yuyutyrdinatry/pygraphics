# Diving back into the world of wx... yay :o

import threading
import wx
import wx.lib.scrolledpanel as scrolled

# Let's attempt to get this working in a style similar to pyglet...
class wxShowFrame(threading.Thread):
    
    class ImagePanel(scrolled.ScrolledPanel):
        def __init__(self, parent):
            scrolled.ScrolledPanel.__init__(self, parent, -1)
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.ipanel = None
        self.pic = None
        
    def run(self):
        self._create_and_init_window()
        self._set_layout_scheme()
        self.app.MainLoop()
        
    def load_image(self, pic):
        if ( self.ipanel is not None ):
            self.pic = pic
            self._update_display()
        else:
            # Wait until the panel is initialized
            while ( self.ipanel is None ):
                True
            self.load_image(pic)
        
    def _update_display(self):
        self.bitmap = self._convert_picture_to_bitmap()
        wx.StaticBitmap(self.ipanel, -1, self.bitmap, (0, 0))
        #self.ipanel.SetScrollbars(1, 1, self.bitmap.GetWidth(), self.bitmap.GetHeight())
        #self.frame.SetSize((self.bitmap.GetWidth(), self.bitmap.GetHeight()))
        
    def _create_and_init_window(self):
        self.app = wx.App()
        
        self.frame = wx.Frame(None, -1, 'Show', (0,0), (100, 100), 
                              wx.DEFAULT_FRAME_STYLE, 'Show')
        self.frame.CenterOnScreen()
        
        self.ipanel = self.ImagePanel(self)
        self.ipanel.CenterOnParent()
        self.ipanel.EnableScrolling(True, True)
        
    def _set_layout_scheme(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.ipanel)
        vbox.Add(hbox, wx.ALL)
        
    def _convert_picture_to_bitmap(self):
        if ( self.pic is not None ):
            pilImage = self.pic.get_image()
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
    
    a = wxShowFrame()
    a.start()
    
    b = picture.Picture(400,200)
    #a.load_image(b)
#    import wx.lib as wxLib
#    import wx.lib.floatcanvas.NavCanvas as wxNC
#    a = wx.App()
#    
#    frame = wx.Frame(None, -1, 'title', (0,0), (400,400), wx.DEFAULT_FRAME_STYLE, 'name')
#    panel = wxNC.NavCanvas(frame, -1, (100,100))
#    frame.Show(True)
#    frame.CenterOnScreen()
#    
#    a.MainLoop()
    
    #dlg.ShowModal()
    #dlg.Destroy()
    #dlg = ID(None, 'C:')
    #dlg.ShowModal()
    #dlg.Destroy()