import Tkinter as tk
import picture
from ImageTk import PhotoImage

from graphics import *
_tkCall = tkCall
_tkExec = tkExec

class ShowWindow(tk.Toplevel):

    def __init__(self):
        tk.Toplevel.__init__(self)
        self.winActive = 0
        
    def _config_window(self):
        width = 300
        height = 300
        
        self.geometry("%dx%d%+d%+d" % (width, height, 200, 200))
        self.wm_minsize(width, height)
        self.wm_maxsize(width, height)
        
        self.canvas = tk.Canvas(r, confine=tk.TRUE)
        self.canvas.config(width=width) 
        self.canvas.config(height=height - 20)
        self.canvas.grid(row=0, column=0)
        self.canvas.pic = None
        self.canvas.photo = None
        self.canvas.image_id = None
        
        self.canvas.pic = picture.Picture(100, 100)
        self.canvas.photo = PhotoImage(self.canvas.pic.get_image())
        
        if ( self.canvas.image_id is None ):
            self.canvas.image_id = self.canvas.create_image((0,0), 
                                                      image=self.canvas.photo, 
                                                      anchor=tk.NW)
        else:
            item = self.canvas.find_withtag(self.canvas.image_id)
            self.canvas.itemconfigure(item, image=self.canvas.photo)
                     
        self.canvas.config(scrollregion=self.canvas.bbox(self.canvas.image_id))
        
    def show(self):
        _tkExec(self._show)

    def _show(self):
        if not self.winActive:
            self._config_window()
            self.winActive = 1
        else:
            self.repaint()
    
    def destroy(self):
        _tkExec(self._destroy)

    def _destroy(self):
        self.pic.windowInactive()
        tk.Toplevel.destroy(self)
        
a = ShowWindow()
a.show()