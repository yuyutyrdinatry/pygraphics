# Diving back into the world of wx... yay :o

import threading
import wx
import wx.lib.scrolledpanel as scrolled

# Let's attempt to get this working in a style similar to pyglet...
class ShowWindow(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        
    def load_image(self, pic):
        if ( self.frame is not None ):
            self.frame.load_image(pic)
        else:
            while ( self.frame is None ):
                True
            self.frame.load_image(pic)
        
    def run(self):
        self.app = wx.App()
        self.frame = ImageFrame()
        self.frame.Show()
        self.app.MainLoop()
        
class ImagePanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        
class ImageFrame(wx.Frame):
    def __init__(self):
        wx.Frame(self, None, -1, 'Show', (0,0), (100,100), 
                 wx.DEFAULT_FRAME_STYLE, 'Show')
        
        self.CenterOnScreen()
        self._create_ipanel()
        self._set_layout_scheme()
    
    def _create_ipanel(self):
        self.ipanel = ImagePanel(self)
        self.ipanel.CenterOnParent()
        self.ipanel.EnableScrolling(True, True)
        
    def _set_layout_scheme(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.ipanel)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, wx.ALL)
        
        self.SetSizer(vbox)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        
    def load_image(self, pic):
        if ( self.ipanel is not None ):
            self.pic = pic
            self._update_display()
        else:
            while ( self.ipanel is None ):
                True
            self.load_image(pic)
        
    def _update_display(self):
        self.bitmap = _convert_picture_to_bitmap(self.pic)
        wx.StaticBitmap(self.frame.ipanel, -1, self.bitmap, (0, 0))
        
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

#a = wxShowFrame()
#a.start()
#
#b = picture.Picture(400,200)