from Tkinter import *
import Image
import ImageDraw
import ImageTk as imtk
import tkFont
import picture

class OpenPictureTool:

    def __init__(self, file_name):
        self.file_name = file_name  #'C:/img_1037.jpg'
        self.picture = picture.make_picture(self.file_name)

    def run_tool(self, safe):
        self.root = Tk()

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

        #
        # create a frame and pack it
        #

        self.frame1 = Frame(self.root)

        self.frame1.pack(side=BOTTOM, fill=X)

        self.root.im = Image.open(self.file_name).convert("RGB")
        self.root.original = self.root.im
        self.root.zoomMult = 1.0

        self.root.photo1 = imtk.PhotoImage(image=self.root.im)

        self.root.title(self.file_name)

        #Canvas for the Image, with scroll bars

        self.canvas1 = Canvas(self.frame1, width=self.root.photo1.width() -
                              1, height=self.root.photo1.height() - 1,
                              cursor="crosshair", borderwidth=0)
        self.root.vbar = Scrollbar(self.frame1)
        self.root.hbar = Scrollbar(self.frame1, orient='horizontal')
        self.root.vbar.pack(side=RIGHT, fill=Y)
        self.root.hbar.pack(side=BOTTOM, fill=X)

        self.canvas1.pack(side="bottom", padx=0, pady=0, anchor=NW, fill=
                          BOTH, expand=YES)
        self.root.vbar.config(command=self.canvas1.yview)  # call on scroll move
        self.root.hbar.config(command=self.canvas1.xview)
        self.canvas1.config(yscrollcommand=self.root.vbar.set)  # call on canvas move
        self.canvas1.config(xscrollcommand=self.root.hbar.set)
        self.drawImage(self.root.im)

        self.canvas1.bind('<Button-1>', self.canvClick)

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

        #
        # start the event loop
        #

        self.root.mainloop()
        if(not safe): #used when not running on darwin(Mac) OS
            sys.exit(0)

    def zoomf(self, factor):

        # zoom in or out in increments

        imgpil = self.root.original
        (wide, high) = imgpil.size

        #root.zoomMult *= factor
        #if factor < 1.0:                     # antialias best if shrink
        #    filter = Image.ANTIALIAS         # also nearest, bilinear
        #else:
        #    filter = Image.BICUBIC

        new = imgpil.resize((int(wide * factor), int(high * factor)))  #, filter)
        self.drawImage(new)

    def restore(self):
        self.drawImage(self.root.original)

    def drawImage(self, imgpil, forcesize=()):
        self.root.im = imgpil
        self.root.photo1 = imtk.PhotoImage(image=imgpil)  # not file=imgpath
        (scrwide, scrhigh) = forcesize or self.root.maxsize()  # wm screen size x,y
        scrhigh -= 115  # leave room for top display/button at max photo size
        imgwide = self.root.photo1.width()  # size in pixels
        imghigh = self.root.photo1.height()  # same as imgpil.size

        fullsize = (0, 0, imgwide, imghigh)  # scrollable
        viewwide = min(imgwide, scrwide)  # viewable
        viewhigh = min(imghigh, scrhigh)

        self.canvas1.delete('all')  # clear prior photo
        self.canvas1.config(height=viewhigh, width=viewwide)  # viewable window size
        self.canvas1.config(scrollregion=fullsize)  # scrollable area size

        self.root.img = self.canvas1.create_image(0, 0, image=self.root.photo1,
                anchor=NW)

        if imgwide <= scrwide and imghigh <= scrhigh:  # too big for display?
            self.root.state('normal')  # no: win size per img
        elif (sys.platform)[:3] == 'win':

            # do windows fullscreen

            self.root.state('zoomed')  # others use geometry( )

    def canvClick(self, event):
        try:
            x = self.canvas1.canvasx(event.x)
            y = self.canvas1.canvasy(event.y)
            if x >= 0 and x < self.root.photo1.width() and y >= 0 and y < \
                self.root.photo1.height():
                tk_rgb = "#%02x%02x%02x" % self.root.im.getpixel((x, y))
                self.canvas2.config(bg=tk_rgb)
                rgb = "R: %d; G: %d; B: %d;" % self.root.im.getpixel((x,
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
            if x >= 0 and x < self.root.photo1.width() and y >= 0 and y < \
                self.root.photo1.height():
                tk_rgb = "#%02x%02x%02x" % self.root.im.getpixel((x, y))
                self.canvas2.config(bg=tk_rgb)
                rgb = "R: %d; G: %d; B: %d;" % self.root.im.getpixel((x,
                        y))
                self.v.set(rgb)
            else:
                rgb = "X,Y Out of Range"
                self.v.set(rgb)
        except ValueError:
            rgb = "X,Y Coordinates must be integers!"
            self.v.set(rgb)
            pass


