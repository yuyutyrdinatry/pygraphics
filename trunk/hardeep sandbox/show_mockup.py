import Tkinter as tk
import picture
from ImageTk import PhotoImage

# This is an attempt to create a show() window for picture display with an
# interactive console.

# This code is very dirty and hacky...but its just to test and see if the
# concept is possible.

class omgz(object):
    
    def __init__(self):
        #=======================================================================
        # Config
        #=======================================================================
        width = 300
        height = 300
        
        #=======================================================================
        # Main Tk Window
        #=======================================================================
        self.r = tk.Tk()
        r = self.r
        r.geometry("%dx%d%+d%+d" % (width, height, 200, 200))
        r.wm_minsize(width, height)
        r.wm_maxsize(width, height)
        
        #=======================================================================
        # Canvas
        #=======================================================================
        r.canvas = tk.Canvas(r, confine=tk.TRUE)
        r.canvas.config(width=width) 
        r.canvas.config(height=height - 20)
        r.canvas.grid(row=0, column=0)
        r.canvas.pic = None
        r.canvas.photo = None
        r.canvas.image_id = None
        
        #=======================================================================
        # Interactive "Console"
        #=======================================================================
        r.str_console = tk.StringVar()
        r.console_entry = tk.Entry(r, textvariable=r.str_console, width=48)
        r.console_entry.grid(row=1, column=0)
        r.console_entry.bind('<KeyPress-KP_Enter>', self._some_bind, True)
        r.console_entry.bind('<KeyPress-Return>', self._some_bind, True)
        
        #=======================================================================
        # Open Pic
        #=======================================================================
        r.canvas.pic = picture.Picture(100, 100)
        r.canvas.photo = PhotoImage(r.canvas.pic.get_image())
        
        if ( r.canvas.image_id is None ):
            r.canvas.image_id = r.canvas.create_image((0,0), 
                                                      image=r.canvas.photo, 
                                                      anchor=tk.NW)
        else:
            item = r.canvas.find_withtag(r.canvas.image_id)
            r.canvas.itemconfigure(item, image=r.canvas.photo)
                     
        r.canvas.config(scrollregion=r.canvas.bbox(r.canvas.image_id))
        r.mainloop()
        
    def update(self, p):
        r = self.r
        r.canvas.photo = p
        item = r.canvas.find_withtag(r.canvas.image_id)
        r.canvas.itemconfigure(item, image=r.canvas.photo)
        r.canvas.config(scrollregion=r.canvas.bbox(r.canvas.image_id))
        
    def _some_bind(self, event):
        data = self.r.str_console.get()
        self.result = compile(data, '<String>', 'exec')
        print 'self.res', self.result
        self.eval = eval(self.result)
        print 'self.eval', self.eval
        self.r.str_console.set(self.eval)
        
a = omgz()