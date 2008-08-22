import time, os, sys
import Tkinter as tk
import tkFileDialog
import Image
import ImageDraw
import ImageTk
import tkFont


####################------------------------------------------------------------
## Exceptions
####################------------------------------------------------------------

import exceptions

class MediaWindowsError(exceptions.Exception):
    """Generic error class for graphics module exceptions."""
    
    def __init__(self, args=None):
        '''Create an Error.'''
        
        self.args = args

# Error message strings
OBJ_ALREADY_DRAWN = "Object currently drawn"
UNSUPPORTED_METHOD = "Object doesn't support operation"
BAD_OPTION = "Illegal option value"
DEAD_THREAD = "Graphics thread quit unexpectedly"

####################------------------------------------------------------------
## Thread support
####################------------------------------------------------------------

from copy import copy
from Queue import Queue
import thread
import atexit

_THREAD_REQUEST = Queue(0) # Queue that can hold an infinite number of items
_THREAD_RESULT = Queue(1) # Queue that can hold one item
_POLL_INTERVAL = 10

_ROOT = None
_THREAD_RUNNING = False

def _mediawindows_thread():
    '''Creates the Tk object as _ROOT, runs _pump() and mainloop.'''
    
    global _ROOT
    _ROOT = tk.Tk()
    _ROOT.withdraw()
    _ROOT.after(_POLL_INTERVAL, _pump)
    _ROOT.mainloop()

def _pump():
    '''Get functions from _THREAD_REQUEST and try executing them. If
    return values are called for put that return in _THREAD_RESULT. If
    an error is raised kill the thread.'''
    
    global _THREAD_RUNNING
    
    while not _THREAD_REQUEST.empty():
        command, returns_value = _THREAD_REQUEST.get()
        try:
            result = command()
            if returns_value:
                _THREAD_RESULT.put(result)
                _THREAD_REQUEST.task_done()
        except:
            _THREAD_RUNNING = False
            if returns_value:
                _THREAD_RESULT.put(None) # release client
            raise # re-raise the exception -- kills the thread
    if _THREAD_RUNNING:
        _ROOT.after(_POLL_INTERVAL, _pump)

def thread_exec_return(f, *args, **kw):
    '''Execute synchronous call to f in the Tk thread. Return it's
    return value. This is to be used from the main thread to communicate
    with the Tk thread. If it is used in the Tk thread it will crash.'''

    if not _THREAD_RUNNING:
        raise MediaWindowsError, DEAD_THREAD
    
    def func():
        return f(*args, **kw)
    
    _THREAD_REQUEST.put((func,True), block=True)
    
    result = _THREAD_RESULT.get(True)
    return result


def thread_exec(f, *args, **kw):
    '''Execute synchronous call to f in the Tk thread. This is to be used
    from the main thread to communicate with the Tk thread. If it is used
    in the Tk thread it will crash.'''

    if not _THREAD_RUNNING:
        raise MediaWindowsError, DEAD_THREAD
    
    def func():
        return f(*args, **kw)
    
    _THREAD_REQUEST.put((func, False), block=True)


def _thread_shutdown():
    '''Shut down the mediawindows thread.'''

    global _THREAD_RUNNING
    _THREAD_RUNNING = False
    time.sleep(.5)

####################------------------------------------------------------------
## Initializer
####################------------------------------------------------------------


def init_mediawindows():
    '''Initialized the mediawindows thread.'''
    
    global _THREAD_RUNNING 
    _THREAD_RUNNING = True
    
    # Fire up the separate Tk thread
    thread.start_new_thread(_mediawindows_thread,())
    
    # Kill the tk thread at exit
    atexit.register(_thread_shutdown)
    


####################------------------------------------------------------------
## Picture Window
####################------------------------------------------------------------
        
class PictureWindow(tk.Canvas):
    """A PictureWindow is a toplevel window for displaying graphics."""

    def __init__(self, title="Graphics Window",
                 width=200, height=200, autoflush=False):
        
        thread_exec_return(self.__init_help, title, width, height, autoflush)
 
    
    def __init_help(self, title, width, height, autoflush):
        
        master = tk.Toplevel(_ROOT)
        master.protocol("WM_DELETE_WINDOW", self.__close_help)
        tk.Canvas.__init__(self, master, width=width, height=height)
        self.master.title(title)
        self.pack()
        master.resizable(0,0)
        self.foreground = "black"
        self.items = []
        self.mouseX = None
        self.mouseY = None
        self.bind("<Button-1>", self._onClick)
        self.height = height
        self.width = width
        self.autoflush = autoflush
        self._mouseCallback = None
        self.trans = None
        self.closed = False
        if autoflush: _ROOT.update()


    def __checkOpen(self):
        if self.closed:
            raise MediaWindowsError, "window is closed"


    def setBackground(self, color):
        """Set background color of the window"""
        self.__checkOpen()
        thread_exec(self.config, bg=color)
        
    def setCoords(self, x1, y1, x2, y2):
        """Set coordinates of window to run from (x1,y1) in the
        lower-left corner to (x2,y2) in the upper-right corner."""
        self.trans = Transform(self.width, self.height, x1, y1, x2, y2)


    def close(self):
        if self.closed: return
        thread_exec_return(self.__close_help)
        
        
    def __close_help(self):
        """Close the window"""
        self.closed = True
        self.master.destroy()
        _ROOT.update()

    def is_closed(self):
        return self.closed

    def __autoflush(self):
        if self.autoflush:
            thread_exec_return(_ROOT.update)
    
    def plot(self, x, y, color="black"):
        """Set pixel (x,y) to the given color"""
        self.__checkOpen()
        xs,ys = self.toScreen(x,y)
        #self.create_line(xs,ys,xs+1,ys, fill=color)
        thread_exec(self.create_line,xs,ys,xs+1,ys,fill=color)
        self.__autoflush()
        
    def plotPixel(self, x, y, color="black"):
        """Set pixel raw (independent of window coordinates) pixel
        (x,y) to color"""
        self.__checkOpen()
    	#self.create_line(x,y,x+1,y, fill=color)
        thread_exec(self.create_line, x,y,x+1,y, fill=color)
        self.__autoflush()
    	
    def flush(self):
        """Update drawing to the window"""
        #self.update_idletasks()
        self.__checkOpen()
        thread_exec_return(self.update_idletasks)
        
    def getMouse(self):
        """Wait for mouse click and return Point object representing
        the click"""
        self.mouseX = None
        self.mouseY = None
        while self.mouseX == None or self.mouseY == None:
            #self.update()
            thread_exec_return(self.update)
            if self.is_closed(): raise MediaWindowsError, "getMouse in closed window"
            time.sleep(.1) # give up thread
        x,y = self.toWorld(self.mouseX, self.mouseY)
        self.mouseX = None
        self.mouseY = None
        return WindowPoint(x,y)

    def checkMouse(self):
        """Return mouse click last mouse click or None if mouse has
        not been clicked since last call"""
        if self.is_closed():
            raise MediaWindowsError, "checkMouse in closed window"
        thread_exec_return(self.update)
        if self.mouseX != None and self.mouseY != None:
            x,y = self.toWorld(self.mouseX, self.mouseY)
            self.mouseX = None
            self.mouseY = None
            return WindowPoint(x,y)
        else:
            return None
            
    def getHeight(self):
        """Return the height of the window"""
        return self.height
        
    def getWidth(self):
        """Return the width of the window"""
        return self.width
    
    def toScreen(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.screen(x,y)
        else:
            return x,y
                      
    def toWorld(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.world(x,y)
        else:
            return x,y
        
    def setMouseHandler(self, func):
        self._mouseCallback = func
        
    def _onClick(self, e):
        self.mouseX = e.x
        self.mouseY = e.y
        if self._mouseCallback:
            self._mouseCallback(WindowPoint(e.x, e.y)) 
      
####################------------------------------------------------------------
## Support Classes
####################------------------------------------------------------------
                
class Transform(object):

    """Internal class for 2-D coordinate transformations"""
    
    def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
        # w, h are width and height of window
        # (xlow,ylow) coordinates of lower-left [raw (0,h-1)]
        # (xhigh,yhigh) coordinates of upper-right [raw (w-1,0)]
        xspan = (xhigh-xlow)
        yspan = (yhigh-ylow)
        self.xbase = xlow
        self.ybase = yhigh
        self.xscale = xspan/float(w-1)
        self.yscale = yspan/float(h-1)
        
    def screen(self,x,y):
        # Returns x,y in screen (actually window) coordinates
        xs = (x-self.xbase) / self.xscale
        ys = (self.ybase-y) / self.yscale
        return int(xs+0.5),int(ys+0.5)
        
    def world(self,xs,ys):
        # Returns xs,ys in world coordinates
        x = xs*self.xscale + self.xbase
        y = self.ybase - ys*self.yscale
        return x,y


# Default values for various item configuration options. Only a subset of
#   keys may be present in the configuration dictionary for a given item
DEFAULT_CONFIG = {"fill":"",
		  "outline":"black",
		  "width":"1",
		  "arrow":"none",
		  "text":"",
		  "justify":"center",
                  "font": ("helvetica", 12, "normal")}

class GraphicsObject(object):

    """Generic base class for all of the drawable objects"""
    # A subclass of GraphicsObject should override _draw and
    #   and _move methods.
    
    def __init__(self, options):
        # options is a list of strings indicating which options are
        # legal for this object.
        
        # When an object is drawn, canvas is set to the GraphWin(canvas)
        #    object where it is drawn and id is the TK identifier of the
        #    drawn shape.
        self.canvas = None
        self.id = None

        # config is the dictionary of configuration options for the widget.
        config = {}
        for option in options:
            config[option] = DEFAULT_CONFIG[option]
        self.config = config
        
    def setFill(self, color):
        """Set interior color to color"""
        self._reconfig("fill", color)
        
    def setOutline(self, color):
        """Set outline color to color"""
        self._reconfig("outline", color)
        
    def setWidth(self, width):
        """Set line weight to width"""
        self._reconfig("width", width)

    def draw(self, graphwin):

        """Draw the object in graphwin, which should be a GraphWin
        object.  A GraphicsObject may only be drawn into one
        window. Raises an error if attempt made to draw an object that
        is already visible."""

        if self.canvas and not self.canvas.is_closed(): raise MediaWindowsError, OBJ_ALREADY_DRAWN
        if graphwin.is_closed(): raise MediaWindowsError, "Can't draw to closed window"
        self.canvas = graphwin
        #self.id = self._draw(graphwin, self.config)
        self.id = thread_exec_return(self._draw, graphwin, self.config)
        if graphwin.autoflush:
            #_ROOT.update()
            thread_exec_return(_ROOT.update)

    def undraw(self):

        """Undraw the object (i.e. hide it). Returns silently if the
        object is not currently drawn."""
        
        if not self.canvas: return
        if not self.canvas.is_closed():
            #self.canvas.delete(self.id)
            thread_exec(self.canvas.delete, self.id)
            if self.canvas.autoflush:
                #_ROOT.update()
                thread_exec_return(_ROOT.update)
        self.canvas = None
        self.id = None

    def move(self, dx, dy):

        """move object dx units in x direction and dy units in y
        direction"""
        
        self._move(dx,dy)
        canvas = self.canvas
        if canvas and not canvas.is_closed():
            trans = canvas.trans
            if trans:
                x = dx/ trans.xscale 
                y = -dy / trans.yscale
            else:
                x = dx
                y = dy
            #self.canvas.move(self.id, x, y)
            thread_exec(self.canvas.move, self.id, x, y)
            if canvas.autoflush:
                #_ROOT.update()
                thread_exec_return(_ROOT.update)
           
    def _reconfig(self, option, setting):
        # Internal method for changing configuration of the object
        # Raises an error if the option does not exist in the config
        #    dictionary for this object
        if not self.config.has_key(option):
            raise MediaWindowsError, UNSUPPORTED_METHOD
        options = self.config
        options[option] = setting
        if self.canvas and not self.canvas.is_closed():
            #self.canvas.itemconfig(self.id, options)
            thread_exec(self.canvas.itemconfig, self.id, options)
            if self.canvas.autoflush:
                #_ROOT.update()
                thread_exec_return(_ROOT.update)

    def _draw(self, canvas, options):
        """draws appropriate figure on canvas with options provided
        Returns Tk id of item drawn"""
        pass # must override in subclass

    def _move(self, dx, dy):
        """updates internal state of object to move it dx,dy units"""
        pass # must override in subclass
         
class WindowPoint(GraphicsObject):
    
    def __init__(self, x, y):
        GraphicsObject.__init__(self, ["outline", "fill"])
        self.setFill = self.setOutline
        self.x = x
        self.y = y
        
        
    def _draw(self, canvas, options):
        x,y = canvas.toScreen(self.x,self.y)
        return canvas.create_rectangle(x,y,x+1,y+1,options)
        
        
    def _move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        
        
    def clone(self):
        other = WindowPoint(self.x,self.y)
        other.config = self.config.copy()
        return other
            
                
    def getX(self): return self.x
    def getY(self): return self.y


class WindowImage(GraphicsObject):

    id_count = 0
    image_cache = {} # tk photoimages go here to avoid GC while drawn 
    
    def __init__(self, point, image):
        
        GraphicsObject.__init__(self, [])
        self.anchor = point.clone()
        self.image_id = WindowImage.id_count
        WindowImage.id_count += 1
        self.img = image


    def _draw(self, canvas, options):
        
        p = self.anchor
        x,y = canvas.toScreen(p.x, p.y)
        self.image_cache[self.image_id] = self.img # save a reference  
        return canvas.create_image(x, y, image=self.img)
    
    
    def _move(self, dx, dy):
        
        self.anchor.move(dx,dy)
    
    
    def get_height(self):
        
        height = thread_exec_return(self.img.height)
        return height
        
        
    def get_width(self):
        
        width = thread_exec_return(self.img.width)
        return width

    
    def undraw(self):
        
        del self.image_cache[self.image_id]  # allow gc of tk photoimage
        GraphicsObject.undraw(self)


    def get_anchor(self):
        
        return self.anchor.clone()
    		
            
    def clone(self):
        
        img_copy = thread_exec_return(self.img.copy)
        other = WindowImage(self.anchor, img_copy)
        other.config = self.config.copy()
        return other


####################------------------------------------------------------------
## Picture Inspector
####################------------------------------------------------------------


class _InspectorBase(tk.Toplevel):

    def __init__(self, pic):
        '''Create an PictureWindow object with Picture pic.'''
        
        tk.Toplevel.__init__(self)
        self.filename = pic.get_filename()
        self.picture = pic.copy()
        self.image = self.picture.get_image()
        self.orig_image = self.image
        self.display()
        


    def display(self):
        '''Run this PictureWindow.'''
                
        self.set_up_display()
        self.set_up_functionalities()
        self.center_window()


    def set_up_display(self):
        '''Set up the display for this PictureWindow.'''
        
        self.pic_frame = tk.Frame(self)
        self.pic_frame.pack(side=tk.BOTTOM, fill=tk.X)      
        
        self.photoimage = ImageTk.PhotoImage(image=self.image)
        self.canvas1 = tk.Canvas(self.pic_frame, 
                              width=self.photoimage.width() - 1,
                              height=self.photoimage.height() - 1,
                              cursor="crosshair", borderwidth=0)
        self.vbar = tk.Scrollbar(self.pic_frame)
        self.hbar = tk.Scrollbar(self.pic_frame, orient='horizontal')
        self.vbar.config(command=self.canvas1.yview)
        self.hbar.config(command=self.canvas1.xview)
        self.canvas1.config(yscrollcommand=self.vbar.set)
        self.canvas1.config(xscrollcommand=self.hbar.set)
        
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas1.pack(anchor=tk.NW)
        self.draw_image(self.image)
        

    def draw_image(self, image):
        '''Update this OpenPictureTool's Canvas with Image image.'''
        
        self.image = image
        self.photoimage = ImageTk.PhotoImage(image=image)
        
        (screen_width, screen_height) = self.maxsize()
        screen_height -= 115  # leave some padding room
        screen_width -= 115
        image_width = self.photoimage.width()
        image_height = self.photoimage.height()

        fullsize = (0, 0, image_width, image_height)  # scrollable region
        view_width = min(image_width, screen_width)  # viewable width
        view_height = min(image_height, screen_height)

        self.canvas1.delete('all')  # clear prior photo
        self.canvas1.config(height=view_height, width=view_width)  # viewable window size
        self.canvas1.config(scrollregion=fullsize)  # scrollable area size
        self.center_window()

        img = self.canvas1.create_image(0, 0, image=self.photoimage, anchor=tk.NW)


    def center_window(self):
        '''Center this PictureWindow on the screen.'''
        
        screen_height = self.winfo_screenheight()
        screen_width = self.winfo_screenwidth()
        window_height = self.winfo_height()
        window_width = self.winfo_width()
        
        new_y_position = (screen_height - window_height) / 2
        new_x_position = (screen_width - window_width) / 2
        new_position = '+%d+%d' % (new_x_position, new_y_position)
        self.geometry(newGeometry=new_position)
    
    
    def set_up_functionalities(self):
        '''Set up all the peripheral functionalities for this PictureWindow.
        Note: This is intended as a method used in inheritance.'''
        
        self.set_up_drag()
    
    def set_up_drag(self):
        '''Set up the dragging capabilities of this PictureWindow.'''
        
        self.mouse_move = False
                
        self.canvas1.bind('<Motion>', self.handler_canvas_movement_move)
        self.canvas1.bind('<Button-1>', self.handler_canvas_movement_start)
        self.canvas1.bind('<ButtonRelease-1>', self.handler_canvas_movement_end)
            
    def handler_canvas_movement_start(self, event):
        '''Set the scan mark of Canvas 1 to the coordinates (x, y) of event.'''
        
        if not self.mouse_move:
            self.canvas1.scan_mark(event.x, event.y)
            self.mouse_move = True
                
    def handler_canvas_movement_move(self, event):
        '''Set the cursor of this PictureWindow to 'hand1' and drag the picture
        to the coordinates (x, y) of event.'''
        
        if self.mouse_move:
            self.canvas1.config(cursor='hand1')
            self.canvas1.scan_dragto(event.x, event.y, gain=1)
        
    def handler_canvas_movement_end(self, event):
        '''Set the cursor of this PictureWindow to crosshairs.'''

        self.canvas1.config(cursor='crosshair')
        self.mouse_move = False


class PictureInspector(_InspectorBase):
    '''A Picture tool that allows you to find information about 
    digital images.
       
    Selecting Pixels:
    To select a pixel drag (click and hold down) the mouse to the position 
    you want and then release it to hold that position's information 
    in the toolbar.
    
    X = the x coordinate of the pixel (counting from the left)
    Y = the y coordinate of the pixel (counting from the top)
    R = the Red value of the pixel (0 to 255)
    G = the Green value of the pixel (0 to 255)
    B = the Blue value of the pixel (0 to 255)
    
    Zooming in/out:
    To Zoom, select the amount of zoom you want from the zoom menu.
    Less than 100% zooms out and more than 100% zooms in. The 100% zoom level will
    always return you to your orginal Picture.'''


    def set_up_functionalities(self):
        
        self.set_up_drag()
        self.canvas1.bind('<Double-Button-1>', self.canvas_click)
        self.set_up_zoommenu()
        self.set_up_fields()
        
            
    def set_up_zoommenu(self):
        '''Set up the zoom menu for this OpenPictureTool.'''
        
        self.top = tk.Menu(self, bd=2)
        self.config(menu=self.top)
        self.zoom = tk.Menu(self.top, tearoff=0)
        self.zoom.add_command(label='25%', command=lambda : self.zoom_by_factor(0.25))
        self.zoom.add_command(label='50%', command=lambda : self.zoom_by_factor(0.5))
        self.zoom.add_command(label='75%', command=lambda : self.zoom_by_factor(0.75))
        self.zoom.add_command(label='100%', command=lambda : self.zoom_by_factor(1.0))
        self.zoom.add_command(label='150%', command=lambda : self.zoom_by_factor(1.5))
        self.zoom.add_command(label='200%', command=lambda : self.zoom_by_factor(2.0))
        self.zoom.add_command(label='500%', command=lambda : self.zoom_by_factor(5.0))
        self.top.add_cascade(label='Zoom', menu=self.zoom)
                     
    def set_up_fields(self):
        
        fields = ('X:', 'Y:')

        self.bind('<Return>', lambda event: self.fetch(self.entries))

        flag = 1
        self.entries = []
        self.v = tk.StringVar()
        self.v.set("R:      G:      B:     ")
        for field in fields:
            row = tk.Frame(self)  # make a new row
            lab = tk.Label(row, width=5, text=field)  # add label, entry
            ent = tk.Entry(row)
            if flag == 1:
                font = tkFont.Font(size=10)
                colorLabel = tk.Label(row, textvariable=self.v, font=font)
                self.canvas2 = tk.Canvas(row, width=35, bd=2, relief=tk.RIDGE,
                        height=20)
            row.pack(side=tk.TOP, fill=tk.X)  # pack row on top
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.LEFT, expand=tk.NO)  # grow horizontal
            if flag == 1:
                colorLabel.pack(side=tk.LEFT, padx=100, pady=1)
                self.canvas2.pack(side=tk.LEFT, padx=2, pady=1)
                flag -= 1
            self.entries.append(ent)

        button1 = tk.Button(row, width=25, overrelief=tk.GROOVE, 
                         bg="lightGrey", text="Enter", 
                         command=lambda : self.fetch(self.entries))
        button1.pack(side=tk.TOP, padx=6, pady=1)


    def zoom_by_factor(self, factor):
        '''Zoom in or out by a factor of float factor.'''
        
        image = self.orig_image
        width, height = image.size
        new = image.resize((int(width * factor), int(height * factor)))
        self.draw_image(new)

    def canvas_click(self, event):
        
        x = self.canvas1.canvasx(event.x)
        y = self.canvas1.canvasy(event.y)
        if 0 <= x < self.photoimage.width() and \
        0 <= y < self.photoimage.height():
            self.update_information(x, y)
        else:
            rgb = "X,Y Out of Range"
            self.v.set(rgb)
            

    def update_information(self, x, y):
        '''Update this OpenPictureTool's display information 
        for coordinate (x, y).'''
        
        canvas_rgb = "#%02x%02x%02x" % self.image.getpixel((x, y))
        self.canvas2.config(bg=canvas_rgb)
        rgb = "R: %d; G: %d; B: %d;" % self.image.getpixel((x, y))
        self.v.set(rgb)
        (entry_x, entry_y) = self.entries
        entry_x.delete(0, tk.END)
        entry_x.insert(0, str(int(x)))
        entry_y.delete(0, tk.END)
        entry_y.insert(0, str(int(y)))


    def fetch(self, entries):
        
        entry_x, entry_y = entries
        try:
            x = int(entry_x.get())
            y = int(entry_y.get())
            if 0 <= x < self.photoimage.width() and \
            0 <= y < self.photoimage.height():
                self.update_information(x, y)
            else:
                rgb = "X,Y Out of Range"
                self.v.set(rgb)
        except ValueError:
            rgb = "X,Y Coordinates must be integers!"
            self.v.set(rgb)


####################------------------------------------------------------------
## Dialogs
####################------------------------------------------------------------


def choose_save_filename():
    '''Prompt user to pick a directory and filename. Return the path
    to the new file. Change the current working directory to the directory 
    where the file chosen by the user is.'''

    path = None
    try:
        path = thread_exec_return(tkFileDialog.asksaveasfilename, parent=_ROOT, initialdir=os.getcwd())
    except:
        pass
    if path:
        os.chdir(os.path.dirname(path))
        return path
    

def choose_file():
    '''Prompt user to pick a file. Return the path to that file. 
    Change the current working directory to the directory 
    where the file chosen by the user is'''
    
    path = None
    try: 
        path = thread_exec_return(tkFileDialog.askopenfilename, parent=_ROOT, initialdir=os.getcwd())
    except:
        pass
    if path:
        os.chdir(os.path.dirname(path))
        return path


def choose_folder():
    '''Prompt user to pick a folder. Return the path to that folder. 
    Change the current working directory to the directory chosen by the user.'''

    path = None
    try:
        path = thread_exec_return(tkFileDialog.askdirectory, parent=_ROOT, initialdir=os.getcwd())
    except:
        pass
    if path:
        os.chdir(os.path.dirname(path))
        return path


def choose_color():
    '''Prompt user to pick a color. Return a RGB Color object.'''

    color = None
    try: 
        color = thread_exec_return(tkFileDialog.askcolor, parent=_ROOT)
    except:
        pass
    if color[0]:
        return Color(color[0][0], color[0][1], color[0][2])