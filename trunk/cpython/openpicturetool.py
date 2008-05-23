from Tkinter import *
import Image
import ImageDraw
import ImageTk
import tkFont
import picture

class OpenPictureTool(object):
    '''A Picture tool that allows you to find information about digital images.
       
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
    always return you to your orginal picture.'''

    def __init__(self, filename=None, image=None):
        '''Create an OpenPictureTool object with Image image or image at file
        filename.'''
        
        if filename:
            self.filename = filename
            self.picture = picture.Picture(filename=self.filename)
        elif image:
            self.filename = ''
            self.picture = picture.Picture(image=image)

    def run_tool(self, safe):
        '''Run this OpenPictureTool.'''
        
        self.root = Tk()
        self.set_up_zoommenu()
        self.set_up_frame()
        self.set_up_canvas()
        self.set_up_fields()
        
        #
        # start the event loop
        #

        self.root.mainloop()
        if(not safe): #used when not running on darwin(Mac) OS
            sys.exit(0)
    
    def set_up_zoommenu(self):
        '''Set up the zoom menu for this OpenPictureTool.'''
        
        self.top = Menu(self.root, bd=2)
        self.root.config(menu=self.top)

        self.zoom = Menu(self.top, tearoff=0)
        self.zoom.add_command(label='25%', command=lambda : self.zoomf(0.25),
                              underline=0)
        self.zoom.add_command(label='50%', command=lambda : self.zoomf(0.5),
                              underline=0)
        self.zoom.add_command(label='75%', command=lambda : self.zoomf(0.75),
                              underline=0)
        self.zoom.add_command(label='100%', command=lambda : self.zoomf(1.0),
                              underline=0)
        self.zoom.add_command(label='150%', command=lambda : self.zoomf(1.5),
                              underline=0)
        self.zoom.add_command(label='200%', command=lambda : self.zoomf(2.0),
                              underline=0)
        self.zoom.add_command(label='500%', command=lambda : self.zoomf(5.0),
                              underline=0)
        self.top.add_cascade(label='Zoom', menu=self.zoom, underline=0)

    def set_up_frame(self):
        '''Set up the Frame for the Picture.'''
        
        self.pic_frame = Frame(self.root)
        self.pic_frame.pack(side=BOTTOM, fill=X)
        
        self.root.image = self.picture.get_image()
        self.root.orig_image = self.root.image
        self.root.photoimage = ImageTk.PhotoImage(image=self.root.image)
        
        self.root.title(self.filename)

    def set_up_canvas(self):
        '''Set up the Canvas in this OpenPictureTool.'''
        
        self.canvas1 = Canvas(self.pic_frame, 
                              width=self.root.photoimage.width() - 1,
                              height=self.root.photoimage.height() - 1,
                              cursor="crosshair", borderwidth=0)
        
        # Scrollbars
        self.root.vbar = Scrollbar(self.pic_frame)
        self.root.hbar = Scrollbar(self.pic_frame, orient='horizontal')
        self.root.vbar.pack(side=RIGHT, fill=Y)
        self.root.hbar.pack(side=BOTTOM, fill=X)

        self.canvas1.pack(side="bottom", padx=0, pady=0, anchor=NW, fill=
                          BOTH, expand=YES)
        self.root.vbar.config(command=self.canvas1.yview)  # call on scroll move
        self.root.hbar.config(command=self.canvas1.xview)
        self.canvas1.config(yscrollcommand=self.root.vbar.set)  # call on canvas move
        self.canvas1.config(xscrollcommand=self.root.hbar.set)
        
        self.draw_image(self.root.image)

        self.canvas1.bind('<Button-1>', self.canvas_click)
    
    def set_up_fields(self):
        
        #Entry fields and Enter button
        fields = ('X:', 'Y:')

        self.root.bind('<Return>', lambda event: self.fetch(self.ents))  #enter key available

        flag = 1
        self.ents = []
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
            ent.pack(side=LEFT, expand=NO, fill=X)  # grow horizontal
            if flag == 1:
                colorLabel.pack(side=LEFT, padx=100, pady=1)
                self.canvas2.pack(side=LEFT, padx=2, pady=1)
                flag -= 1
            self.ents.append(ent)

        button1 = Button(row, width=25, overrelief=GROOVE, bg=
                         "lightGrey", text="Enter", command=lambda : \
                         self.fetch(self.ents)).pack(side=TOP, padx=6,
                pady=1, anchor=CENTER, fill=BOTH)



    def zoomf(self, factor):
        '''Zoom in or out by a factor of float factor.'''
        
        image = self.root.orig_image
        (wide, high) = image.size
        new = image.resize((int(wide * factor), int(high * factor)))
        self.draw_image(new)

    def restore(self):
        self.draw_image(self.root.orig_image)

    def draw_image(self, image, forcesize=()):
        self.root.image = image
        self.root.photoimage = ImageTk.PhotoImage(image=image)  # not file=imgpath
        (scrwide, scrhigh) = forcesize or self.root.maxsize()  # wm screen size x,y
        scrhigh -= 115  # leave room for top display/button at max photo size
        imgwide = self.root.photoimage.width()  # size in pixels
        imghigh = self.root.photoimage.height()  # same as image.size

        fullsize = (0, 0, imgwide, imghigh)  # scrollable
        viewwide = min(imgwide, scrwide)  # viewable
        viewhigh = min(imghigh, scrhigh)

        self.canvas1.delete('all')  # clear prior photo
        self.canvas1.config(height=viewhigh, width=viewwide)  # viewable window size
        self.canvas1.config(scrollregion=fullsize)  # scrollable area size

        self.root.img = self.canvas1.create_image(0, 0, image=self.root.photoimage,
                anchor=NW)

        if imgwide <= scrwide and imghigh <= scrhigh:  # too big for display?
            self.root.state('normal')  # no: win size per img
        elif (sys.platform)[:3] == 'win':

            # do windows fullscreen

            self.root.state('zoomed')  # others use geometry( )

    def canvas_click(self, event):
        
        try:
            x = self.canvas1.canvasx(event.x)
            y = self.canvas1.canvasy(event.y)
            if x >= 0 and x < self.root.photoimage.width() and y >= 0 and y < \
                self.root.photoimage.height():
                tk_rgb = "#%02x%02x%02x" % self.root.image.getpixel((x, y))
                self.canvas2.config(bg=tk_rgb)
                rgb = "R: %d; G: %d; B: %d;" % self.root.image.getpixel((x,
                        y))
                self.v.set(rgb)
                (evX, evY) = self.ents
                evX.delete(0, END)
                evX.insert(0, str(int(x)))
                evY.delete(0, END)
                evY.insert(0, str(int(y)))
            else:
                rgb = "X,Y Out of Range"
                self.v.set(rgb)
        except ValueError:
            pass

    #do at Button press or Enter key press

    def fetch(self, entries):
        (strX, strY) = entries
        try:
            x = int(strX.get())
            y = int(strY.get())
            if x >= 0 and x < self.root.photoimage.width() and y >= 0 and y < \
                self.root.photoimage.height():
                tk_rgb = "#%02x%02x%02x" % self.root.image.getpixel((x, y))
                self.canvas2.config(bg=tk_rgb)
                rgb = "R: %d; G: %d; B: %d;" % self.root.image.getpixel((x,
                        y))
                self.v.set(rgb)
            else:
                rgb = "X,Y Out of Range"
                self.v.set(rgb)
        except ValueError:
            rgb = "X,Y Coordinates must be integers!"
            self.v.set(rgb)
            pass

if __name__ == '__main__':
    p = picture.Picture(100, 100)
    p.clear(picture.salmon)
    p.show_in_picture_tool()

