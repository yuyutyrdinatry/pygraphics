import threading
import wx
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

class wxShow(wx.Frame):
    def __init__(self, parent=None, id=-1, title="Show Window"):
        wx.Frame.__init__(self, parent, id, title)
        self.parent = parent
        self.__init_window()

    def __init_window(self):
        self.Show(True)
        
    def display(self, pic):
        self.pic = pic
        self.bitmap = self._convert_picture_to_bitmap()
        self._update_display()
        
    def _update_display(self):
        wx.StaticBitmap(self, -1, self.bitmap, (0, 0))
        
    def _convert_picture_to_bitmap(self):
        if ( self.pic is not None ):
            pilImage = self.pic.get_image()
            image = _piltoimage(pilImage)
            return wx.BitmapFromImage(image)
        
def _piltoimage(pil, alpha=True):
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

def _imagetopil(image):
    """Convert wx.Image to PIL Image."""
    pil = Image.new('RGB', (image.GetWidth(), image.GetHeight()))
    pil.fromstring(image.GetData())
    return pil
        
if __name__ == "__main__":
    a = ShowWrapperThread()
    a.start()
    
    import picture
    b = picture.Picture(200,200)
    a.update_picture(b)