import Tkinter as tk
import threading
from time import time
from ImageTk import PhotoImage

class ShowWrapperThread(threading.Thread):
    '''Wraps the ShowOMatic into it's own thread.'''
    
    def set_loop_bind(self, bind):
        self.bind = bind
        
    def run(self):
        '''Runs when the thread is started. Executes the local function bind.'''
        self.bind()
    
class ShowTimerThread(threading.Thread):
    '''Timer thread to update the show window.'''
    stop = False
        
    def run(self):
        '''Runs when the thread is started.'''
        
        # Create local variables of all functions, variables, etc... for speed
        get_time = time
        poll_interval = self.poll_interval
        update = self.update_bind
        
        a = get_time()
        while ( not self.stop ):
            delta_t = get_time() - a 
            if ( delta_t >= poll_interval ):
                a = get_time()
                update()
                
    def set_update_bind(self, bind):
        self.update_bind = bind
    
    def set_poll_interval(self, interval=1):
        '''Set the local poll_interval to the int interval which is the interval
        in which to update the canvas in seconds.'''
        self.poll_interval = interval
    
    def end(self):
        '''Set the local boolean self.stop to True.'''
        self.stop = True

class ShowOMatic(tk.Frame):
    
    def __init__(self, pic=None, poll=None):
        '''Create main application window, put a frame inside it, run all the 
        initialization methods and finally update the main window title.
        
        If we are given the optional picture pic, then we'll display it right
        away in the window. The optional int poll specifies how many seconds the
        timer thread should wait before attempting an automatic update of the
        show window.'''
        
        # Note: by calling the tk.Frame constructor, it will also create a main
        # Tk window called master (i.e. self.master)
        tk.Frame.__init__(self, None)
        self.grid()
        self.__init_vars()
        self.__initialize_window_main()
        self.__init_canvas_mover()
        
        if ( poll is not None ):
            self.poll = max(1, poll)
            
        self.show(pic)
            
    def show(self, pic=None):
        '''Show the given picture Pic in the ShowOMatic window. If the window is
        already open, then update the displayed pic. If pic is not given, and
        there is already an opened pic, update the display for that pic.'''
        
        if ( pic is not None ):
            self.pic = pic
            self.photo = None
        
        self.__threads_start()
        self.__update_canvas()
            
    # Initial configuratio and creation helpers --------------------------------
    def __init_vars(self):
        '''Initliaze local instance variables to default states.'''
        
        self.pic = None
        self.photo = None
        self.thread_started = None
        self.poll = None
        
        self.scroll_width = 16
        self.scroll_spacing = self.scroll_width + 5
        
        self.window_dim = [0,0] # window dimensions [w, h]
        self.window_min_dim = [100, 100] # minimum window dimensions [w, h]
        
        self.thread_show = None
        self.thread_poll = None
            
    def __initialize_window_main(self):
        '''Create the main program window.'''
        
        # Main window config
        min = self.window_min_dim
        self.master.geometry("%dx%d%+d%+d" % (min[0], min[1], 0, 0))
        self.master.wm_minsize(min[0], min[1])
        
        # Add and configure canvas + scroll bars
        self.__create_canvas()
        self.__create_scrollbars()
        self.__attach_scrollbars_to_canvas()
        
        # Add event handlers
        self.master.bind('<Configure>', self.handler_configure_window_main, True)
        self.master.protocol('WM_DELETE_WINDOW', 
                             self.handler_window_main_destroy)
        
    def __create_canvas(self):
        '''Create the canvas object on the main window.'''
        
        self.canvas = tk.Canvas(self.master, confine=tk.TRUE)
        self.canvas.config(width=100 - self.scroll_spacing) 
        self.canvas.config(height=100 - self.scroll_spacing)
        self.canvas.grid(row=0, column=0)
        self.canvas.image_id = None
        
    def __create_scrollbars(self):
        '''Create scroll bars and position them around the canvas in the main
        application window.'''
        
        self.scroll_Y = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        self.scroll_Y.config(width=self.scroll_width)
        self.scroll_Y.grid(row=0, column=1, sticky=tk.NS)
        
        self.scroll_X = tk.Scrollbar(self.master, orient=tk.HORIZONTAL)
        self.scroll_X.config(width=self.scroll_width)
        self.scroll_X.grid(row=1, column=0, sticky=tk.EW)
        
    def __attach_scrollbars_to_canvas(self):
        '''Attach the scrollbars to the canvas so the scrollbars can scroll
        through the canvas.'''
        
        self.scroll_Y.config(command=self.canvas.yview)
        self.scroll_X.config(command=self.canvas.xview)
        self.canvas["xscrollcommand"] = self.scroll_X.set
        self.canvas["yscrollcommand"] = self.scroll_Y.set
       
    # Update helpers -----------------------------------------------------------
    def __update_canvas(self):
        '''Show or update the current Picture on the canvas. 
        
        If there is already a PhotoImage shown on the canvas, then overwrite its
        data with the current Picture. Also resize the canvas and set its
        scroll region.'''
        
        try:
            c = self.canvas
            self.__update_photo()
            
            if ( c.image_id is None ):
                c.image_id = c.create_image((0,0), image=self.photo, anchor=tk.NW)
            else:
                item = c.find_withtag(c.image_id)
                c.itemconfigure(item, image=self.photo)
            
            self.__update_canvas_and_scroll_sizes()
        except tk.TclError:
            # This will almost always occur because the canvas is destroyed
            # before a thread stops and finishes working on it. So this will
            # just suppress the possibly confusing message for new programmers.
            pass
        except ValueError:
            # Same as above
            pass
        
    def __update_photo(self):
        '''Update the photo representation of the local pic.'''
        if ( self.pic is not None ):
            self.photo = PhotoImage(self.pic.get_image())
        
    def __update_canvas_and_scroll_sizes(self, event=None):
        '''Update the size of the canvas in comparison to the main window 
        size.'''
        
        c = self.canvas
        if ( ( self.photo is None or self.pic is None ) and event is not None ):
            w = event.width - self.scroll_spacing
            h = event.height - self.scroll_spacing
        else:
            w, h = self.__get_min_canvas_dim()
        
        c.config(width=w, height=h)
        if ( c.image_id is not None ):
            c.config(scrollregion=c.bbox(c.image_id))
        
    # Event Handlers -----------------------------------------------------------
    def handler_window_main_destroy(self):
        '''Bind for the WM_DELETE_WINDOW protocal for the main window.'''
        
        if ( self.thread_poll is not None ):
            self.thread_poll.end()
            self.thread_poll = None
        
        self.thread_show = None
        self.master.destroy()
        
    def handler_configure_window_main(self, event):
        '''Bind for the <Configure> event on the main application window.
        
        Resize the canvas and set the scrolling regions as the main application
        window is resized.'''
        
        if ( event.height and event.width and (event.widget == self.master)):
            self.window_dim = [event.width, event.height]
            self.__update_canvas_and_scroll_sizes(event)
            
    # Get Helpers --------------------------------------------------------------
    def __get_min_canvas_dim(self):
        '''With a picture open, return the int width and int height in a tuple 
        that the canvas should be set to by taking the minimum size of either
        the main_window_dimensions - the scroll_spacing, or the size of 
        dimensions open picture.'''
        
        w, h = self.window_dim
        scroll = self.scroll_spacing
        
        if ( self.photo is not None ):
            photo_w = self.photo.width()
            photo_h = self.photo.height()
        else:
            photo_w = photo_h = 0
        
        new_w = min(w - scroll, photo_w)
        new_h = min(h - scroll, photo_h)
            
        return (new_w, new_h)
    
    # Threading ----------------------------------------------------------------
    def __threads_start(self):
        '''Start a new thread if it has not already been created and then launch
        the Tk window in that thread. Will also create the timer thread if the
        local int poll has been specified and it has not already been
        created.'''
        if ( self.thread_show is None ):
            self.thread_show = ShowWrapperThread()
            self.thread_show.set_loop_bind(self.threads_mainloop)
            self.thread_show.start()
        
        if ( self.poll is not None and self.thread_poll is None ):
            self.thread_poll = ShowTimerThread()
            self.thread_poll.set_poll_interval(self.poll)
            self.thread_poll.set_update_bind(self.threads_update)
            self.thread_poll.start()
    
    # Threading : Binds --------------------------------------------------------
    def threads_mainloop(self):
        '''The mainloop to run in a thread.'''
        self.mainloop()
    
    def threads_update(self):
        '''Used to update the displayed picture from a thread.'''
        self.__update_canvas()
        
    # Mouse-based Canvas Movement ----------------------------------------------
    def __init_canvas_mover(self):
        self.canvas_mouse_bind = ["3", "2", "1"]
        
        self.mouse_start = [0, 0]
        self.mouse_move = False
        
        m_start = self.__handler_canvas_movement_start
        m_move = self.__handler_canvas_movement_move
        m_end = self.__handler_canvas_movement_end
        
        # Set the binds for all the specified mouse buttons
        self.canvas.bind('<Motion>', m_move, True)
        for button in self.canvas_mouse_bind:
            self.canvas.bind('<Button-%s>' % button, m_start, True)
            self.canvas.bind('<ButtonRelease-%s>' % button, m_end, True)
            
    def __handler_canvas_movement_start(self, event):
        '''Bound to the <Button-X> event on the main application canvas. Where X
        is the mouse buttons defined in self.canvas_mouse_bind. 
        
        Get the current mouse position relative to the top left of the screen
        and store it in the canvas.mouse_start list. Then set canvas.mouse_move
        to True to enabled movement.'''
        if ( event.widget == self.canvas and self.pic is not None ):
            self.mouse_start = [event.x_root, event.y_root]
            self.mouse_move = True
            self.canvas.config(cursor='hand1')
            
    def __handler_canvas_movement_move(self, event):
        '''Bound to the <Motion> event on the main application canvas.
        
        If canvas.mouse_move is set to True, move the canvas relative to the
        mouse position and current scrollbar position. Also changes cursor
        to "hand1".'''
        if ( event.widget == self.canvas and self.pic is not None 
             and self.mouse_move ):
            canvas = self.canvas
            s_x, s_y = self.mouse_start
            
            d_x = (s_x - event.x_root) / float(self.pic.get_width())
            d_y = (s_y - event.y_root) / float(self.pic.get_height())
            d_x += self.scroll_X.get()[0]
            d_y += self.scroll_Y.get()[0]
            
            self.mouse_end = [event.x, event.y]
            canvas.xview(tk.MOVETO, d_x)
            canvas.yview(tk.MOVETO, d_y)
            self.mouse_start = [event.x_root, event.y_root]
            
    def __handler_canvas_movement_end(self, event):
        '''Bound to the <ButtonRelease-X> event on the main application canvas.
        Where X is the mouse buttons defined in self.canvas_mouse_bind.
        
        Disable mouse movement by setting canvas.mouse_move to False and then
        reset cursor back to "arrow".'''
        if ( event.widget == self.canvas and self.pic is not None ):
            self.mouse_move = False
            self.canvas.config(cursor='arrow')