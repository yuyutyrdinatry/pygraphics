from Tkinter import *
import Image
import ImageDraw
import ImageTk
import picture
import tkFont

# Add help button
class PictureWindow(object):

    def __init__(self, pic):
        '''Create an PictureWindow object with Picture pic.'''
        
        self.filename = pic.get_filename()
        self.picture = pic
        self.image = pic.get_image()
        self.orig_image = self.image


    def run_window(self):
        '''Run this PictureWindow.'''
        
        self.root = Tk()
        self.root.title(self.filename)
        
        self.set_up_display()
        self.set_up_functionalities()
        self.root.update_idletasks()
        self.center_window()

        self.root.mainloop()    

    def set_up_display(self):
        '''Set up the display for this PictureWindow.'''
        
        self.pic_frame = Frame(self.root)
        self.pic_frame.pack(side=BOTTOM, fill=X)      
        
        self.photoimage = ImageTk.PhotoImage(image=self.image)
        self.canvas1 = Canvas(self.pic_frame, 
                              width=self.photoimage.width() - 1,
                              height=self.photoimage.height() - 1,
                              cursor="crosshair", borderwidth=0)
        self.vbar = Scrollbar(self.pic_frame)
        self.hbar = Scrollbar(self.pic_frame, orient='horizontal')
        self.vbar.config(command=self.canvas1.yview)
        self.hbar.config(command=self.canvas1.xview)
        self.canvas1.config(yscrollcommand=self.vbar.set)
        self.canvas1.config(xscrollcommand=self.hbar.set)
        
        self.vbar.pack(side=RIGHT, fill=Y)
        self.hbar.pack(side=BOTTOM, fill=X)
        self.canvas1.pack(anchor=NW)
        self.draw_image(self.image)
        

    def draw_image(self, image):
        '''Update this OpenPictureTool's Canvas with Image image.'''
        
        self.image = image
        self.photoimage = ImageTk.PhotoImage(image=image)
        
        (screen_width, screen_height) = self.root.maxsize()
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

        img = self.canvas1.create_image(0, 0, image=self.photoimage, anchor=NW)


    def center_window(self):
        '''Center this PictureWindow on the screen.'''
        
        screen_height = self.root.winfo_screenheight()
        screen_width = self.root.winfo_screenwidth()
        window_height = self.root.winfo_height()
        window_width = self.root.winfo_width()
        
        new_y_position = (screen_height - window_height) / 2
        new_x_position = (screen_width - window_width) / 2
        new_position = '+%d+%d' % (new_x_position, new_y_position)
        self.root.geometry(newGeometry=new_position)
    
    
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


class PictureInspector(PictureWindow):
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
        
        self.top = Menu(self.root, bd=2)
        self.root.config(menu=self.top)
        self.zoom = Menu(self.top, tearoff=0)
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

        self.root.bind('<Return>', lambda event: self.fetch(self.entries))

        flag = 1
        self.entries = []
        self.v = StringVar()
        self.v.set("R:      G:      B:     ")
        for field in fields:
            row = Frame(self.root)  # make a new row
            lab = Label(row, width=5, text=field)  # add label, entry
            ent = Entry(row)
            if flag == 1:
                font = tkFont.Font(size=10)
                colorLabel = Label(row, textvariable=self.v, font=font)
                self.canvas2 = Canvas(row, width=35, bd=2, relief=RIDGE,
                        height=20)
            row.pack(side=TOP, fill=X)  # pack row on top
            lab.pack(side=LEFT)
            ent.pack(side=LEFT, expand=NO)  # grow horizontal
            if flag == 1:
                colorLabel.pack(side=LEFT, padx=100, pady=1)
                self.canvas2.pack(side=LEFT, padx=2, pady=1)
                flag -= 1
            self.entries.append(ent)

        button1 = Button(row, width=25, overrelief=GROOVE, 
                         bg="lightGrey", text="Enter", 
                         command=lambda : self.fetch(self.entries))
        button1.pack(side=TOP, padx=6, pady=1)


    def zoom_by_factor(self, factor):
        '''Zoom in or out by a factor of float factor.'''
        
        image = self.orig_image
        width, height = image.size
        new = image.resize((int(width * factor), int(height * factor)))
        self.draw_image(new)
        self.root.update_idletasks()
        self.center_window()


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
        entry_x.delete(0, END)
        entry_x.insert(0, str(int(x)))
        entry_y.delete(0, END)
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
    

if __name__ == '__main__':
    p = picture.Picture(filename='/Users/chris/Pictures/Pictures I Took/Annie(Smaller).jpg')
    tool = PictureInspector(p)
    tool.run_window()
