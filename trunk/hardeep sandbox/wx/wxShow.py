import threading
import wx
import os
import time

class ShowWrapperThread(threading.Thread):
    '''Wraps wxShow's MainLoop into it's own thread.'''
    
    def __init__(self):
        threading.Thread.__init__(self, None, self.run, "wxShow")
        self.setDaemon(1)
        self.__init_vars()
    
    def __init_vars(self):
        self.pic = None
        self.app = None
        self.frame = None
        
    def run(self):
        # TODO: use wx.PySimpleApp() for MacOS
        if ( os.sys.platform == 'darwin' ):
            self.app = wx.PySimpleApp(redirect=False)
        else:
            self.app = wx.App(redirect=False)
        self.frame = wxShow()
        self.app.MainLoop()
        
    def update_picture(self, pic):
        if ( self.frame is not None ):
            self.pic = pic
            self._update_window()
        else:
            time.sleep(1)
            self.update_picture(pic)
        
    def _update_window(self):
        self.frame.display(self.pic)
        
class DisplayCanvas(wx.ScrolledWindow):
    def __init__(self, *args, **kwargs):
        wx.ScrolledWindow.__init__(self, *args, **kwargs)

class wxShow(wx.Frame):
    def __init__(self, parent=None, id=-1, title="Show Window"):
        wx.Frame.__init__(self, parent, id, title)
        self.parent = parent
        self.__init_window()

    def __init_window(self):
        self.Show(True)
        self._set_sizer()
        self._create_scroller()
        self.Center()
        
    def _set_sizer(self):
        self.box = wx.GridBagSizer()
        self.box.AddGrowableCol(0)
        self.box.AddGrowableRow(0)
        
        self.SetSizerAndFit(self.box)
        self.SetAutoLayout(True)
        self.SetSizeHints(200, 200)
        
    def _create_scroller(self):
        self.dc = DisplayCanvas(self, -1)
        self.dc.EnableScrolling(True, True)
        self.box.Add(self.dc, (0,0), (1,1), wx.EXPAND)
        
    def display(self, pic):
        self.pic = pic
        self.bitmap = self._convert_picture_to_bitmap()
        self._update_display()
        
    def _update_display(self):
        wx.StaticBitmap(self.dc, -1, self.bitmap, (0, 0))
        self.dc.SetScrollbars(1, 1, self.bitmap.GetWidth(), self.bitmap.GetHeight())
        self.SetSize((self.bitmap.GetWidth(), self.bitmap.GetHeight()))
        
    def _convert_picture_to_bitmap(self):
        if ( self.pic is not None ):
            pilImage = self.pic.get_image()
            image = _pil_to_image(pilImage)
            return wx.BitmapFromImage(image)
        
def _pil_to_image(pil, alpha=True):
    """Convert PIL Image to wx.Image."""
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

def _image_to_pil(image):
    """Convert wx.Image to PIL Image."""
    pil = Image.new('RGB', (image.GetWidth(), image.GetHeight()))
    pil.fromstring(image.GetData())
    return pil
        
if __name__ == "__main__":
    a = ShowWrapperThread()
    a.start()
    
    import picture
    b = picture.Picture(400,200)
    a.update_picture(b)