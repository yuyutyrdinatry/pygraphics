#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Media Wrappers for "Introduction to Media Computation"
# Started: Mark Guzdial, 2 July 2002
#
# 7 December Lots of new stuff
#               dumped wxwindows because it hates threads and really despises pygame
#               tkinter used as alternative this is python standard for windowing
#               add PIL as a requirement to allow for easy image export and save to jpeg
#               converted pick_a_file, pick_a_folder, pick_a_color to TKDialog pop-ups
#               moved initialization out of the class init and into the main import
#
# NOTE:
#               due to issues with Tkinter and PyGame, we can not initialize pygame.display
#               without causing Tkinter dialogs to mess up.  For the time being,
#               pygame.display should not be initialized (all the other functions work,
#               ie. with pygame.surface).  If you run into code which requires
#               pygame.display to be initialized, please find an alternative.
#
#               - (surface.convert requires pygame.display to be inited and should not
#                       be used, use the PIL Image module instead)
#
# June 14, 2007 modified file, commented out Movie, Sound, Turtle
# Signed: Leo Kaliazine
#
#

#from Image import fromstring

from math import sqrt

#from Queue import *
#from threading import *

from Tkinter import *

#from tkCommonDialog import Dialog
#import cStringIO

import Image
import ImageDraw
import ImageFont
import ImageTk as imtk

#import ImageTk
#import inspect
#import Numeric

import os

#import pygame
#import re
#import struct

import sys
import time
import tkColorChooser
import tkFileDialog
import tkMessageBox
import tkFont

#import tkSnack

import user
import thread

##
## Global vars -------------------------------------------------------
##

ver = "1.1"
default_frequency = 22050
default_sample_size = -16  # negative denotes signed number of bits
default_num_channels = 1  # stereo or mono

#pygame.mixer.pre_init(default_frequency, default_sample_size, (default_num_channels > 1))
#pygame.font.init()
#pygame.mixer.init()
#default_font = pygame.font.SysFont("times", 24)

default_font = ImageFont.load_default()

#top = Tk()
#top.withdraw()
# set up the tkSnack sound library
#tkSnack.initializeSnack(top)

media_folder = user.home + os.sep

##
## Global misc functions -------------------------------------------------------
##


def open_picture_tool():
    OpenPictureTool()


def version():
    global ver
    return ver


def set_media_path():
    global media_folder
    file = pick_a_folder()
    media_folder = file
    print "New media folder: " + media_folder


def get_media_path(filename):
    global media_folder
    file = media_folder + filename
    if not os.path.isfile(file):
        print "Note: There is no file at " + file
    return file


def pick_a_file(**options):
    root = Tk()
    root.title("Choose File")
    root.focus_force()
    root.geometry("0x0")
#   root.geometry("+100+200")
    root.attributes("-alpha",0.0)
    #root.withdraw()
    path = tkFileDialog.askopenfilename()
    #root.mainloop()
    root.destroy()
    return path

#def askopen(root):
#     root.path = tkFileDialog.askopenfilename()
#     root.destroy()
#     #return path

def pick_a_folder(**options):
    global media_folder
    folder = tkFileDialog.askdirectory()
    if folder == '':
        folder = media_folder
    return folder


def pick_a_color(**options):
    color = tkColorChooser.askcolor()
    new_color = Color(color[0][0], color[0][1], color[0][2])
    return new_color


#And for those who think of things as folders (5/14/03 AW)


def set_media_folder():
    global media_folder
    file = pick_a_folder()
    media_folder = file
    print "New media folder: " + media_folder


def get_media_folder(filename):
    global media_folder
    file = media_folder + filename
    if not os.path.isfile(file) or not os.path.isdir(file):
        print "Note: There is no file at " + file
    return file


def get_short_path(filename):
    dirs = filename.split(os.sep)
    if len(dirs) < 1:  # does split() ever get to this stage?
        return "."
    elif len(dirs) == 1:
        return dirs[0]
    else:
        return dirs[len(dirs) - 2] + os.sep + dirs[len(dirs) - 1]


def quit():
    sys.exit(0)


##
## COLOR -----------------------------------------------------------------------
##


class Color:

    def __init__(self, r, g, b):
        self.r = int(r) % 256
        self.g = int(g) % 256
        self.b = int(b) % 256

    def __str__(self):
        return "color r=" + str(self.get_red()) + " g=" + str(self.get_green()) + \
            " b=" + str(self.get_blue())

    def __repr__(self):
        return "Color(" + str(self.get_red()) + ", " + str(self.get_green()) + \
            ", " + str(self.get_blue()) + ")"

    def __sub__(self, color):
        return Color(self.r - color.r, self.g - color.g, self.b - color.b)

    def __add__(self, color):
        return Color(self.r + color.r, self.g + color.g, self.b + color.b)

    def __eq__(self, newcolor):
        return self.get_red() == newcolor.get_red() and self.get_green() == \
            newcolor.get_green() and self.get_blue() == newcolor.get_blue()

    def __ne__(self, newcolor):
        return not self.__eq__(newcolor)

    def distance(self, color):
        r = pow(self.r - color.r, 2)
        g = pow(self.g - color.g, 2)
        b = pow(self.b - color.b, 2)
        return sqrt(r + g + b)

    def difference(self, color):
        return self - color

    def get_rgb(self):

        #changed wat's returned from an [] to a tuple

        return [self.r, self.g, self.b]

    def set_rgb(self, atuple):
        self.r = int(atuple[0]) % 256
        self.g = int(atuple[1]) % 256
        self.b = int(atuple[2]) % 256

    def get_red(self):
        return self.r

    def get_green(self):
        return self.g

    def get_blue(self):
        return self.b

    def set_red(self, value):
        self.r = int(value) % 256

    def set_green(self, value):
        self.g = int(value) % 256

    def set_blue(self, value):
        self.b = int(value) % 256

    def make_lighter(self):
        self.r = int((255 - self.r) * .35 + self.r)
        self.g = int((255 - self.g) * .35 + self.g)
        self.b = int((255 - self.b) * .35 + self.b)

    def make_darker(self):
        self.r = int(self.r * .65)
        self.g = int(self.g * .65)
        self.b = int(self.b * .65)


##
## Color Constants -------------------------------------------------------------
##

aliceblue = Color(240, 248, 255)
antiquewhite = Color(250, 235, 215)
aqua = Color(0, 255, 255)
aquamarine = Color(127, 255, 212)
azure = Color(240, 255, 255)
beige = Color(245, 245, 220)
bisque = Color(255, 228, 196)
black = Color(0, 0, 0)
blanchedalmond = Color(255, 235, 205)
blue = Color(0, 0, 255)
blueviolet = Color(138, 43, 226)
brown = Color(165, 42, 42)
burlywood = Color(222, 184, 135)
cadetblue = Color(95, 158, 160)
chartreuse = Color(127, 255, 0)
chocolate = Color(210, 105, 30)
coral = Color(255, 127, 80)
cornflowerblue = Color(100, 149, 237)
cornsilk = Color(255, 248, 220)
crimson = Color(220, 20, 60)
cyan = Color(0, 255, 255)
darkblue = Color(0, 0, 139)
darkcyan = Color(0, 139, 139)
darkgoldenrod = Color(184, 134, 11)
darkgray = Color(169, 169, 169)
darkgreen = Color(0, 100, 0)
darkkhaki = Color(189, 183, 107)
darkmagenta = Color(139, 0, 139)
darkolivegreen = Color(85, 107, 47)
darkorange = Color(255, 140, 0)
darkorchid = Color(153, 50, 204)
darkred = Color(139, 0, 0)
darksalmon = Color(233, 150, 122)
darkseagreen = Color(143, 188, 143)
darkslateblue = Color(72, 61, 139)
darkslategray = Color(47, 79, 79)
darkturquoise = Color(0, 206, 209)
darkviolet = Color(148, 0, 211)
deeppink = Color(255, 20, 147)
deepskyblue = Color(0, 191, 255)
dimgray = Color(105, 105, 105)
dodgerblue = Color(30, 144, 255)
firebrick = Color(178, 34, 34)
floralwhite = Color(255, 250, 240)
forestgreen = Color(34, 139, 34)
fuchsia = Color(255, 0, 255)
gainsboro = Color(220, 220, 220)
ghostwhite = Color(248, 248, 255)
gold = Color(255, 215, 0)
goldenrod = Color(218, 165, 32)
gray = Color(128, 128, 128)
green = Color(0, 128, 0)
greenyellow = Color(173, 255, 47)
honeydew = Color(240, 255, 240)
hotpink = Color(255, 105, 180)
indianred = Color(205, 92, 92)
indigo = Color(75, 0, 130)
ivory = Color(255, 255, 240)
khaki = Color(240, 230, 140)
lavender = Color(230, 230, 250)
lavenderblush = Color(255, 240, 245)
lawngreen = Color(124, 252, 0)
lemonchiffon = Color(255, 250, 205)
lightblue = Color(173, 216, 230)
lightcoral = Color(240, 128, 128)
lightcyan = Color(224, 255, 255)
lightgoldenrodyellow = Color(250, 250, 210)
lightgreen = Color(144, 238, 144)
lightgrey = Color(211, 211, 211)
lightpink = Color(255, 182, 193)
lightsalmon = Color(255, 160, 122)
lightseagreen = Color(32, 178, 170)
lightskyblue = Color(135, 206, 250)
lightslategray = Color(119, 136, 153)
lightsteelblue = Color(176, 196, 222)
lightyellow = Color(255, 255, 224)
lime = Color(0, 255, 0)
limegreen = Color(50, 205, 50)
linen = Color(250, 240, 230)
magenta = Color(255, 0, 255)
maroon = Color(128, 0, 0)
mediumaquamarine = Color(102, 205, 170)
mediumblue = Color(0, 0, 205)
mediumorchid = Color(186, 85, 211)
mediumpurple = Color(147, 112, 219)
mediumseagreen = Color(60, 179, 113)
mediumslateblue = Color(123, 104, 238)
mediumspringgreen = Color(0, 250, 154)
mediumturquoise = Color(72, 209, 204)
mediumvioletred = Color(199, 21, 133)
midnightblue = Color(25, 25, 112)
mintcream = Color(245, 255, 250)
mistyrose = Color(255, 228, 225)
moccasin = Color(255, 228, 181)
navajowhite = Color(255, 222, 173)
navy = Color(0, 0, 128)
oldlace = Color(253, 245, 230)
olive = Color(128, 128, 0)
olivedrab = Color(107, 142, 35)
orange = Color(255, 165, 0)
orangered = Color(255, 69, 0)
orchid = Color(218, 112, 214)
palegoldenrod = Color(238, 232, 170)
palegreen = Color(152, 251, 152)
paleturquoise = Color(175, 238, 238)
palevioletred = Color(219, 112, 147)
papayawhip = Color(255, 239, 213)
peachpuff = Color(255, 218, 185)
peru = Color(205, 133, 63)
pink = Color(255, 192, 203)
plum = Color(221, 160, 221)
powderblue = Color(176, 224, 230)
purple = Color(128, 0, 128)
red = Color(255, 0, 0)
rosybrown = Color(188, 143, 143)
royalblue = Color(65, 105, 225)
saddlebrown = Color(139, 69, 19)
salmon = Color(250, 128, 114)
sandybrown = Color(244, 164, 96)
seagreen = Color(46, 139, 87)
seashell = Color(255, 245, 238)
sienna = Color(160, 82, 45)
silver = Color(192, 192, 192)
skyblue = Color(135, 206, 235)
slateblue = Color(106, 90, 205)
slategray = Color(112, 128, 144)
snow = Color(255, 250, 250)
springgreen = Color(0, 255, 127)
steelblue = Color(70, 130, 180)
tan = Color(210, 180, 140)
teal = Color(0, 128, 128)
thistle = Color(216, 191, 216)
tomato = Color(255, 99, 71)
turquoise = Color(64, 224, 208)
violet = Color(238, 130, 238)
wheat = Color(245, 222, 179)
white = Color(255, 255, 255)
whitesmoke = Color(245, 245, 245)
yellow = Color(255, 255, 0)
yellowgreen = Color(154, 205, 50)

##
## PICTURE FRAME ---------------------------------------------------------------

#class PictureFrame(Toplevel):
#
#    def __init__(self, picture):
#        Toplevel.__init__(self)
#        self.title(picture.title)
#        self.pic = picture

#    def destroy(self):
#        self.pic.window_inactive()
#        Toplevel.destroy(self)

##
## PICTURE ---------------------------------------------------------------------
##


class Picture:

    def __init__(self, auto_repaint=False):
        self.title = "Unnamed"
        self.disp_image = None
        self.win_active = 0

#        self.__auto_repaint = auto_repaint
#        self.visible_frame = False
#        self.__event_bindings = {}
        # bind the mouse event to show the pixel information
        #       self.add_event_handler("<Button-1>", self.do_pick_color)
        #       self.add_event_handler("<B1-Motion>", self.do_pick_color)

    def __initialize_picture(self, surf, filename, title):
        self.surf = surf

        # we get the pixels array from the surface

        self.pixels = surf.load()  #pygame.surfarray.pixels3d(self.surf)

        #self.p = []

        #for i in range(surf.size[0]):
        #    self.p.append([])
        #    for j in range(surf.size[1]):
        #        self.p[i].append(list(self.pixels[i,j]))

        #self.pixels = self.p

        self.filename = filename
        self.title = title

#        self.__update()

#    def set_auto_repaint(self, boolean):
#        self.__auto_repaint = boolean
#        self.__update()

#    def window_inactive(self):
#        del self.disp_image, self.item, self.canvas
#        self.win_active = 0
#        self.visible_frame = False

    def create_image(self, width, height):

        # fail if dimensions are invalid

        if width < 0 or height < 0:
            raise ValueError("create_image(" + str(width) + ", " + str(height) +
                             "): Invalid image dimensions")
        else:
            self.__initialize_picture(Image.new("RGB", (width, height)),
                    '', 'None')

            #self.__initialize_picture(pygame.Surface((width, height)), '', 'None')

    def load_image(self, filename):
        global media_folder
        if not os.path.isabs(filename):
            filename = media_folder + filename

        # fail if file does not exist

        if not os.path.isfile(filename):
            raise ValueError("load_image(" + filename +
                             "): No such file")
        else:
            from Image import open
            mode = "RGB"
            image = open(filename).convert(mode)
            size = image.size
            data = image.tostring()

            # initialize this picture with new properties

            self.__initialize_picture(image, filename, get_short_path(filename))

#    def copy_from_image(self, picture, x=0, y=0, width=None, height=None):
#        print x, y, width, height
#    # copies and image from another picture, replacing this one
#        # note that the coordinates are one based
#        # chnaged coordinates to zero based
#        # copy the other picture's image
#        image = picture.get_image().copy()
#    # crop to the dimensions specified
#        image_width = picture.get_width()
#        image_height = picture.get_height()
#        # throw exceptions if the values are invalid
#        if (x < 0 or y < 0 or x >= image_width or y >= image_height):
#            raise ValueError(('Invalid x/y coordinates specified'))
#        # width || height < 1 implies a full image copied (maybe with warning)
#        if (width == None and height == None):
#            width = image_width
#            height = image_height
#        # fail if either is None, or they are < 1
#        elif (width == None or height == None or width < 1 or height < 1):
#            raise ValueError(('Invalid width/height specified'))
#        # get/bound the actual image coordinates
#        x1 = x
#        y1 = y
#        x2 = x1+min(width, image_width-x1)
#        y2 = y1 + min(height, image_height-y1)
#        # get the sub image with the dimensions specified [x1,y1,x2,y1)
#        box = (x1, y1, x2, y2)
#        image = image.crop(box)
#        # get the image properties
#        mode = image.mode
#        size = image.size
#        data = image.tostring()
#        image = Image.fromstring(mode, size, data)
#        # initialize this picture with new properties
#        self.__initialize_picture(image, picture.filename, picture.title)

    def crop(self, x1, y1, x2, y2):
        maxX = self.get_width()
        None
        maxY = self.get_height()
        None
        if not 0 <= x1 <= maxX or not 0 <= y1 <= maxY or not x1 < x2 <= \
            maxX or not y1 < y2 <= maxY:
            raise ValueError('Invalid width/height specified')

        image = self.surf.crop((x1, y1, x2, y2))
        self.__initialize_picture(image, picture.filename, picture.title)

#    def overlay_image(self, picture, x=0, y=0):
#        if x == 0:
#            # center x
#            x = (self.get_width()/2)-(picture.get_width()/2)+1
#        if y == 0:
#            # center y
#            y = (self.get_height()/2)-(picture.get_height()/2)+1
#        # blit the other image
#        # note that we must unlock both image surfaces
#        self.surf.unlock()
#        picture.surf.unlock()
#        self.surf.blit(picture.surf, (x-1, y-1))
#        picture.surf.lock()
#        self.surf.lock()
##        self.__update()

    def clear(self, color=black):

        # clears the picture pixels to black

        self.set_pixels(color)

    def __str__(self):
        return "Picture, filename " + self.filename + " height " + str(self.get_height()) + \
            " width " + str(self.get_width())

#    def __update(self):
#        if self.visible_frame and self.__auto_repaint:
#            self.repaint()

#    def repaint(self):
#        if self.win_active:
#            self.canvas.delete(self.item)
#            self.disp_image = ImageTk.PhotoImage(self.get_image())
#            self.item = self.canvas.create_image(0, 0, image=self.disp_image, anchor='nw')
#            self.canvas.pack()
#            self.canvas.update()
#            self.frame.title(self.title)
#        else:
#            self.show()

    def show(self):
        i = 1
        p = thread.start_new(self.showchild, (i, ))
        time.sleep(0.1)

        #if raw_input() == 'c': pass

    def showchild(self, tid):

        #os.execlp('python', 'python', 'test.py') # overlay program

        self.surf.show()

        #assert False, 'error starting program'               # shouldn't return
#        if not self.win_active:
#            self.frame = PictureFrame(self)
#            self.canvas = Canvas(self.frame, width=self.get_width(),
#                height=self.get_height(), highlightthickness=0)
#
#            self.disp_image = ImageTk.PhotoImage(self.get_image())
#            self.item = self.canvas.create_image(0, 0, image=self.disp_image, anchor='nw')
#            self.canvas.pack()
#            self.win_active = 1
#            self.visible_frame = True
#            # bind all events
#            for event_str, callback in self.__event_bindings.items():
#                self.canvas.bind(event_str, callback)
#        else:
#            self.repaint()

    def do_pick_color(self, event):
        x = event.x + 1
        y = event.y + 1
        if 0 < x and x <= self.get_width() and 0 < y and y < self.get_height():
            pixel = self.get_pixel(x, y)
            print pixel
            None

#    def hide(self):
#        if self.win_active:
#            self.frame.destroy()

    def set_title(self, title):
        self.title = title

#        self.__update()

    def get_title(self):
        return self.title

    def get_image(self):

        # seems to return a PIL image of the same dimensions
        #data = pygame.image.tostring(self.surf, "RGB", 0)
        #image = fromstring("RGB", (self.get_width(), self.get_height()), data)
        #data = self.surf.tostring()
        #image = Image.fromstring("RGB", (self.get_width(), self.get_height()), data)

        if self.get_height() == 0 and self.get_width() == 0:  #TODO this is temp fix for UnitTest
            raise ValueError
        return self.surf

    def get_width(self):
        return (self.surf.size)[0]

    def get_height(self):
        return (self.surf.size)[1]

    def get_pixel(self, x, y):
        return Pixel(self, x, y)

        #return Pixel(self.pixels,x,y)

    def get_pixels(self):
        collect = []

        # we want the width and the height inclusive since Pixel() is one based
        # we increase the ranges so that we don't have to add in each iteration
        #Changed to 0-based!

        for x in range(0, self.get_width()):
            for y in range(0, self.get_height()):
                collect.append(Pixel(self, x, y))

                #collect.append(Pixel(self.pixels,x,y))

        return collect

    def set_pixels(self, color):
        """set all the pixels in this picture to a given color"""

        try:
            image = Image.new(self.surf.mode, self.surf.size, tuple(color.get_rgb()))
            self.__initialize_picture(image, self.filename, self.title)
        except:

            #self.surf.fill(color.get_rgb())
#            self.__update()

            raise AttributeError('set_pixels(color): Picture has not yet been initialized.')

    def write_to(self, filename):
        if not os.path.isabs(filename):
            filename = media_folder + filename

        #pygame.image.save(self.surf, filename)
        #image = self.get_image()
        #image.save(filename, None)

        self.surf.save(filename)

    # TODO: add bounds checks for all the following functions to ensure that they are one based
    # draw stuff on pictures

    def add_rect_filled(self, acolor, x, y, w, h):

        #pygame.draw.rect(self.surf, acolor.get_rgb(), pygame.Rect(x-1, y-1, w, h))

        draw = ImageDraw.Draw(self.surf)
        draw.rectangle([x, y, x + w, y + h], outline=tuple(acolor.get_rgb()),
                       fill=tuple(acolor.get_rgb()))
        del draw

#        self.__update()

    def add_rect(self, acolor, x, y, w, h, width1=1):

        #pygame.draw.rect(self.surf, acolor.get_rgb(), pygame.Rect(x-1, y-1, w, h), width)

        draw = ImageDraw.Draw(self.surf)
        draw.rectangle([x, y, x + w, y + h], outline=tuple(acolor.get_rgb()))
        del draw

#        self.__update()

    # Draws a polygon on the image.

    def add_polygon(self, acolor, point_list):

        #pygame.draw.polygon(self.surf, acolor.get_rgb(), point_list, 1)

        draw = ImageDraw.Draw(self.surf)
        draw.polygon(point_list, outline=tuple(acolor.get_rgb()))
        del draw

#        self.__update()

    def add_polygon_filled(self, acolor, point_list):

        #pygame.draw.polygon(self.surf, acolor.get_rgb(), point_list, 0)

        draw = ImageDraw.Draw(self.surf)
        draw.polygon(point_list, outline=tuple(acolor.get_rgb()), fill=
                     tuple(acolor.get_rgb()))
        del draw

#        self.__update()

    def add_oval_filled(self, acolor, x, y, w, h):

        #pygame.draw.ellipse(self.surf, acolor.get_rgb(), pygame.Rect(x-1, y-1, w, h))

        draw = ImageDraw.Draw(self.surf)
        draw.ellipse([x, y, x + w, y + h], outline=tuple(acolor.get_rgb()),
                     fill=tuple(acolor.get_rgb()))
        del draw

#        self.__update()

    def add_oval(self, acolor, x, y, w, h):

        #pygame.draw.ellipse(self.surf, acolor.get_rgb(), pygame.Rect(x-1, y-1, w, h), 1)

        draw = ImageDraw.Draw(self.surf)
        draw.ellipse([x, y, x + w, y + h], outline=tuple(acolor.get_rgb()))
        del draw

#        self.__update()

    def add_arc_filled(self, acolor, x, y, w, h, start, end):

        #this is an estimation def needs to be done another way but I need to figure out how
        #if w > h:
        #    pygame.draw.arc(self.surf, acolor.get_rgb(), Rect(x, y, w, h), start, angle, h/2)
        #else:
        #    pygame.draw.arc(self.surf, acolor.get_rgb(), Rect(x, y, w, h), start, angle, w/2)
#        self.__update()

        draw = ImageDraw.Draw(self.surf)
        draw.arc([x, y, x + w, y + h], start, end, outline=tuple(acolor.get_rgb()),
                 fill=tuple(acolor.get_rgb()))
        del draw

    def add_arc(self, acolor, x, y, w, h, start, end):

        #pygame.draw.arc(self.surf, acolor.get_rgb(), Rect(x, y, w, h), start, angle)
#        self.__update()

        draw = ImageDraw.Draw(self.surf)
        draw.arc([x, y, x + w, y + h], start, end, outline=tuple(acolor.get_rgb()))
        del draw

    def add_line(self, acolor, x1, y1, x2, y2, width1=1):

        #pygame.draw.line(self.surf, acolor.get_rgb(), [x1-1, y1-1], [x2-1, y2-1], width)
#        self.__update()

        draw = ImageDraw.Draw(self.surf)
        draw.line([x1, y1, x2, y2], fill=tuple(acolor.get_rgb()), width=
                  width1)
        del draw

    def add_text(self, acolor, x, y, string):
        global default_font
        self.add_text_with_style(acolor, x, y, string, default_font)

#        self.__update()

    def add_text_with_style(self, acolor, x, y, string, font1):

        # add the text with the specified font
        #text_surf = font.render(string, True, acolor.get_rgb())
        #self.surf.unlock()
        #self.surf.blit(text_surf, (x-1, y-1))
        #self.surf.lock()
#       self.__update()

        draw = ImageDraw.Draw(self.surf)
        draw.text((x, y), text=string, fill=tuple(acolor.get_rgb()),
                  font=font1)
        del draw


#    def add_event_handler(self, tk_event_str, callback):
#        # see: http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
#        # for more information
#        self.__event_bindings[tk_event_str] = callback
#        if self.win_active:
#            self.canvas.bind(tk_event_str, callback)

#    def remove_event_handler(self, tk_event_str):
#        if tk_event_str in self.__event_bindings:
#            del self.__event_bindings[tk_event_str]
#            if self.win_active:
#                self.canvas.unbind(tk_event_str)

#    def remove_all_event_handlers(self):
#        if self.win_active:
#            for event_str, callback in self.__event_bindings.items():
#                    self.canvas.unbind(event_str)
#        self.__event_bindings.clear()

#
# PIXEL ------------------------------------------------------------------------
#


class Pixel:

    def __init__(self, picture, x, y):

        if not picture.__class__ == Picture:
            raise ValueError("Pixel(picture, x, y): picture input is not a Picture")

        len_x = picture.get_width()  #len(picture)
        len_y = picture.get_height()  #len(picture[0])
        if x <= -1 * len_x or x >= len_x or y <= -1 * len_y or y >= \
            len_y:
            raise IndexError
        if len_x > 0 and len_y > 0:
            self.x = x % len_x  #self.x = (x - 1) % len_x
            self.y = y % len_y  #self.y = (y - 1) % len_y

            # we still want to fail if the accessible indices are out of wrap-around bounds so we
            # can not use self.x, and self.y below
            #self.pix = [picture.pixels[x-1,y-1]]#picture[x-1][y-1]

            self.pix = picture
        else:

            #self.pix.pixels[x-1,y-1]=(255,255,255)

            raise ValueError('Invalid image dimensions (' + str(len_x) +
                             ", " + str(len_y) + ")")

    def __str__(self):
        return "Pixel, color=" + str(self.get_color())

    def set_red(self, r):
        if 0 <= r and r <= 255:
            (self.pix.pixels)[self.x, self.y] = (r, (self.pix.pixels)[self.x,
                    self.y][1], (self.pix.pixels)[self.x, self.y][2])
        else:

            #self.pix[0] = r

            raise ValueError('Invalid red component value (' + str(r) +
                             '), expected value within [0, 255]')

    def set_green(self, g):
        if 0 <= g and g <= 255:
            (self.pix.pixels)[self.x, self.y] = ((self.pix.pixels)[self.x,
                    self.y][0], g, (self.pix.pixels)[self.x, self.y][2])
        else:

            #self.pix[1] = g

            raise ValueError('Invalid green component value (' + str(g) +
                             '), expected value within [0, 255]')

    def set_blue(self, b):
        if 0 <= b and b <= 255:
            (self.pix.pixels)[self.x, self.y] = ((self.pix.pixels)[self.x,
                    self.y][0], (self.pix.pixels)[self.x, self.y][1], b)
        else:

            #self.pix[2] = b

            raise ValueError('Invalid blue component value (' + str(b) +
                             '), expected value within [0, 255]')

    def get_red(self):
        return int((self.pix.pixels)[self.x, self.y][0])

    def get_green(self):
        return int((self.pix.pixels)[self.x, self.y][1])

    def get_blue(self):
        return int((self.pix.pixels)[self.x, self.y][2])

    def get_color(self):
        return Color(self.get_red(), self.get_green(), self.get_blue())

    def set_color(self, color):
        self.set_red(color.get_red())
        self.set_green(color.get_green())
        self.set_blue(color.get_blue())

    def get_x(self):
        return self.x  # + 1

    def get_y(self):
        return self.y  # + 1


##
## Picture Tool ----------------------------------------------------------------
##


class OpenPictureTool:

    def __init__(self, file_name):
        self.file_name = file_name  #'C:/img_1037.jpg'
        self.picture = make_picture(self.file_name)

#p = pickAFile()
#p = makePicture(p)
#openPictureTool(p)
#fileName = 'C:\img_1037.jpg'
#fileName = 'C:\image.gif'

#
#import sys
#import Tkinter as tk
#from PIL import Image
#

    def run_tool(self):
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

        #zoom.add_separator()
        #zoom.add_command(label='Restore',    command=restore, underline=0)

        self.top.add_cascade(label='Zoom', menu=self.zoom, underline=0)

        #
        # create a frame and pack it
        #

        self.frame1 = Frame(self.root)

        #

        self.frame1.pack(side=BOTTOM, fill=X)

        #

        #
        # pick a (small) image file you have in the working directory ...
        #
        #root.photo1 = tk.PhotoImage(file="C:\Image.gif")

        self.root.im = Image.open(self.file_name).convert("RGB")
        self.root.original = self.root.im
        self.root.zoomMult = 1.0

        #saveimage = im

        self.root.photo1 = imtk.PhotoImage(image=self.root.im)  #file="C:\img_1037.jpg")

        #savephoto = root.photo1

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

        #img = canvas1.create_image(0,0,image=root.photo1,anchor=tk.NW)

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

        #canvas = canvas1

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

        #print (scrwide, scrhigh), imgpil.size

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
                evX.insert(0, str(x))
                evY.delete(0, END)
                evY.insert(0, str(y))
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

                #row.update_idletasks()

                rgb = "X,Y Out of Range"
                self.v.set(rgb)
        except ValueError:
            pass


##
## Global picture functions ----------------------------------------------------
##


def open_picture_tool(filename):
    """filename: a string represeting the location and name of picture
       Allows you to find information about digital images.
       
       The PictureTool's Toolbar:
        Once you have opened an image, you can view information about its individual
        pixels by looking at the toolbar. To select a pixel drag (click and hold down)
        the mouse to the position you want and then release it to hold that position's
        information in the toolbar.
        The following information in the toolbar changes to reflect the properties of
        the pixel you selected:
        X = the x coordinate of the pixel (its horizontal position, counting from the left)
        Y = the y coordinate of the pixel (its vertical position, counting from the top)
        R = the Red value of the pixel (0 to 255)
        G = the Green value of the pixel (0 to 255)
        B = the Blue value of the pixel (0 to 255)
        In addition, the box at the far right displays the color of the pixel.
       Zooming in/out:
        To Zoom, select the amount of zoom you want from the zoom menu.
        Less than 100% zooms out and more than 100% zooms in. The 100% zoom level will
        always return you to your orginal picture. """

    tool = OpenPictureTool(filename)
    p = thread.start_new_thread(tool.run_tool, ())


def make_picture(filename):
    """filename: a string represeting the location and name of picture
       Creates a picture."""

    picture = Picture()
    picture.load_image(filename)
    try:
        w = picture.get_width()
        return picture
    except:
        print "Was unable to load the image in " + filename + \
            "\nMake sure it's a valid image file."


# Maybe


def make_empty_picture(width, height):
    """width: the width of the picture
       height:  the height of the picture
       Generates a blank picture"""

    picture = Picture()
    picture.create_image(width, height)
    return picture


def crop_picture(picture, x1, y1, x2, y2):
    """picture: the picture to be cropped
       x1: defines left pixel coordinate
       y1: defines upper pixel coordinate
       x2: defines right pixel coordinate
       y2: defines lower pixel coordinate.
       Replaces picture with a rectangular region from the current picture.
       Note coordinates are zero-based so to get a 50x50 image starting from
       top left corner the coordinates would be: 0,0,49,49"""

    if not picture.__class__ == Picture:
        raise ValueError("crop_picture(picture,x1,y1,x2,y2): First input is not a picture")
    picture.crop(x1, y1, x2 + 1, y2 + 1)


#def duplicate_picture(picture):
#    if not picture.__class__ == Picture:
#        raise ValueError("duplicate_picture(picture): First input is not a picture")
#    new_picture = Picture()
#    new_picture.copy_from_image(picture)
#    return new_picture

#def make_style(fontname, fontsize=10, bold=False, italic=False):
#    # try to make a font style with the given parameters
#    global default_font
#    try:
#        return pygame.font.SysFont(fontname, fontsize, bold, italic)
#    except:
#        print "make_style(fontname,fontsize,bold,italic): No such font found"
#        return default_font

# Maybe


def set_pixels(picture, color):
    """picture: the picture to be modified
       color: the color to which all the pixels will be set
       Sets all the pixels of the picture given as first argument
       to the color given as second argument"""

    if not picture.__class__ == Picture:
        raise ValueError("set_pixels(picture,color): First input is not a picture")
    if not color.__class__ == Color:
        raise ValueError("set_pixels(picture,color): Second input is not a color.")
    return picture.set_pixels(color)


def get_pixel(picture, x, y):
    """picture: the picture you want to get the pixel from
       x: the x-coordinate of the pixel you want
       y: the y-coordinate of the pixel you want
       Takes a picture, an x position and a y position (two numbers),
       and returns the Pixel object at that point in the picture."""

    if not picture.__class__ == Picture:
        raise ValueError("get_pixel(picture,x,y): Input is not a picture")
    return picture.get_pixel(x, y)


def get_pixels(picture):
    '''picture: the picture you want to get the pixels from
       returns: a list of all the pixels in the picture
       Takes a picture as input and returns the sequence of
       Pixel objects in the picture. This is another name for "getPixels".'''

    if not picture.__class__ == Picture:
        raise ValueError("get_pixels(picture): Input is not a picture")
    return picture.get_pixels()


def get_width(picture):
    """picture: the picture you want to get the width of
       returns: the width of the picture
       Takes a picture as input and returns its length in
       the number of pixels left-to-right in the picture."""

    if not picture.__class__ == Picture:
        raise ValueError("get_width(picture): Input is not a picture")
    return picture.get_width()


def get_height(picture):
    """picture: the picture you want to get the height of
       returns: the height of the picture
       Takes a picture as input and returns its length in the
       number of pixels top-to-bottom in the picture."""

    if not picture.__class__ == Picture:
        raise ValueError("get_height(picture): Input is not a picture")
    return picture.get_height()


def show(picture, title=None):
    """picture: Picture to be displayed
       title(optional): Title of the image to be displayed
       Displays the picture. On Unix platforms, this method saves the
       image to a temporary PPM file, and calls the xv utility.
       On Windows, it saves the image to a temporary BMP file,
       and uses the standard BMP display utility to show it."""

    if not picture.__class__ == Picture:
        raise ValueError("show(picture): Input is not a picture")
    picture.show()


#def repaint(picture):
#    if not picture.__class__ == Picture:
#        raise ValueError("repaint(picture): Input is not a picture")
#    picture.repaint()

# Maybe


def add_line(picture, x1, y1, x2, y2, acolor):
    """picture: the picture you want to draw the line on 
       x1: the x position you want the line to start 
       y1: the y position you want the line to start
       x2: the x position you want the line to end 
       y2: the y position you want the line to end
       acolor: the color you want to draw in 
       Takes a picture, a starting (x, y) position (two numbers), and an
       ending (x, y) position (two more numbers, four total) and draws a
       line from the starting point to the ending point in the picture."""

    if not picture.__class__ == Picture:
        raise ValueError("add_line(picture,x1,y1,x2,y2): Input is not a picture")
    picture.add_line(acolor, x1, y1, x2, y2)


# Maybe


def add_text(picture, x1, y1, string, acolor):
    """picture: the picture you want to add the text to
       x1: the x-coordinate where you want to start writing the text
       y1: the y-coordinate where you want to start writing the text
       string: s string containing the text you want written
       acolor: the color you want to draw in
       Takes a picture, an x position and a y position (two numbers),
       and some text as a string, which will get drawn into the picture,
       in the specified color."""

    if not picture.__class__ == Picture:
        raise ValueError("add_text(picture,x1,y1,string): Input is not a picture")
    picture.add_text(acolor, x1, y1, string)


# Maybe


def add_rect(picture, x, y, w, h, acolor):
    """picture: the picture you want to draw the rectangle on
       x: the x-coordinate of the upper left-hand corner of the rectangle
       y: the y-coordinate of the upper left-hand corner of the rectangle
       w: the width of the rectangle
       h: the height of the rectangle
       acolor: the color you want to draw in
       Takes a picture, a starting (x, y) position (two numbers), and a width
       and height (two more numbers, four total) then draws a rectangle in
       outline of the given width and height with the position (x, y) as the
       upper left corner."""

    if not picture.__class__ == Picture:
        raise ValueError("add_rect(picture,x,y,w,h): Input is not a picture")
    picture.add_rect(acolor, x, y, w, h)


# Maybe


def add_rect_filled(picture, x, y, w, h, acolor):
    """picture: the picture you want to draw the rectangle on
       x: the x-coordinate of the upper left-hand corner of the rectangle
       y: the y-coordinate of the upper left-hand corner of the rectangle
       w: the width of the rectangle
       h: the height of the rectangle
       acolor: the color you want to draw in 
       Takes a picture, a starting (x, y) position (two numbers), and a width
       and height (two more numbers, four total) then draws a filled rectangle
       of the given width, height and color with the position (x, y) as the
       upper left corner."""

    if not picture.__class__ == Picture:
        raise ValueError("add_rect_filled(picture,x,y,w,h,acolor): Input is not a picture")
    picture.add_rect_filled(acolor, x, y, w, h)


# Maybe


def add_polygon(picture, point_list, acolor):
    """picture: the picture you want to draw the polygon on
       pointlist: a list containing vertices xy coordinates
                  (ex. [x1,y1,x2,y2,x3,y3])
                  It should contain at least three coordinate pairs.
       acolor: the color you want to draw in 
       Takes a picture, draws an outline (not filled) of a polygon in the
       given color with the sides being lines connecting the given vertices"""

    if not picture.__class__ == Picture:
        raise ValueError("add_polygon(picture,point_list,acolor): Input is not a picture")
    picture.add_polygon(acolor, point_list)


# Maybe


def add_polygon_filled(picture, pointlist, acolor):
    """picture: the picture you want to draw the polygon on
       pointlist: a list containing vertices xy coordinates
                  (ex. [x1,y1,x2,y2,x3,y3])
                  It should contain at least three coordinate pairs.
       acolor: the color you want to draw in 
       Takes a picture, draws a filled polygon in the given color with
       the sides being lines connecting the given vertices"""

    if not picture.__class__ == Picture:
        raise ValueError("add_polygon_filled(picture,pointlist,acolor): Input is not a picture")
    picture.add_polygon_filled(acolor, pointlist)


def write_picture_to(pict, filename):
    '''pict: the picture you want to be written out to a file
       path: the path to the file you want the picture written to
       Takes a picture and a file name (string) as input, then writes
       the picture to the file as a JPEG. (Be sure to end the filename
       in ".jpg" for the operating system to understand it well.)'''

    if not pict.__class__ == Picture:
        raise ValueError("write_picture_to(pict,filename): Input is not a picture")
    pict.write_to(filename)


    #if not os.path.exists(filename):
    #       print "write_picture_to(pict,filename): Path is not valid"
    #       raise ValueError

##
## Global pixel functions ------------------------------------------------------
##


def set_red(pixel, value):
    """pixel: the pixel you want to set the red value in.
       value: a number (0 - 255) for the new red value of the pixel
       Takes in a Pixel object and a value (between 0 and 255) and sets
       the redness of that pixel to the given value."""

    if not pixel.__class__ == Pixel:
        raise ValueError("set_red(pixel,value): Input is not a pixel")
    pixel.set_red(value)


def get_red(pixel):
    """pixel: the pixel you want to get the amount of red from
       returns: the red value of the pixel
       Takes a Pixel object and returns the value (between 0 and 255)
       of the amount of redness in that pixel."""

    if not pixel.__class__ == Pixel:
        raise ValueError("get_red(pixel): Input is not a pixel")
    return pixel.get_red()


def set_blue(pixel, value):
    """pixel: the pixel you want to set the blue value in.
       value: a number (0 - 255) for the new blue value of the pixel
       Takes in a Pixel object and a value (between 0 and 255) and sets
       the blueness of that pixel to the given value."""

    if not pixel.__class__ == Pixel:
        raise ValueError("set_blue(pixel,value): Input is not a pixel")
    pixel.set_blue(value)


def get_blue(pixel):
    """pixel: the pixel you want to get the amount of blue from
       returns: the blue value of the pixel
       Takes a Pixel object and returns the value (between 0 and 255)
       of the amount of blueness in that pixel."""

    if not pixel.__class__ == Pixel:
        raise ValueError("get_blue(pixel): Input is not a pixel")
    return pixel.get_blue()


def set_green(pixel, value):
    """pixel: the pixel you want to set the green value in.
       value: a number (0 - 255) for the new green value of the pixel
       Takes in a Pixel object and a value (between 0 and 255) and sets
       the greeness of that pixel to the given value."""

    if not pixel.__class__ == Pixel:
        raise ValueError("set_green(pixel,value): Input is not a pixel")
    pixel.set_green(value)


def get_green(pixel):
    """pixel: the pixel you want to get the amount of green from
       returns: the green value of the pixel
       Takes a Pixel object and returns the value (between 0 and 255)
       of the amount of greenness in that pixel."""

    if not pixel.__class__ == Pixel:
        raise ValueError("get_green(pixel): Input is not a pixel")
    return pixel.get_green()


def get_color(pixel):
    """pixel: the pixel you want to extract the color from
       returns: a color, the color from the pixel
       Takes a Pixel and returns the Color object at that pixel."""

    if not pixel.__class__ == Pixel:
        raise ValueError("get_color(pixel): Input is not a pixel")
    return pixel.get_color()


def set_color(pixel, color):
    """pixel: the pixel you want to set the color of
       color: the color you want to set the pixel to
       Takes in a pixel and a color, and sets the pixel to the provided color."""

    if not pixel.__class__ == Pixel:
        raise ValueError("set_color(pixel,color): Input is not a pixel.")
    if not color.__class__ == Color:
        raise ValueError("set_color(pixel,color): Input is not a color.")
    pixel.set_color(color)


def get_x(pixel):
    """pixel: the pixel you want to find the x-coordinate of
       returns: the x-coordinate of the pixel
       Takes in a pixel object and returns the x position of
       where that pixel is in the picture."""

    if not pixel.__class__ == Pixel:
        raise ValueError("get_x(pixel): Input is not a pixel")
    return pixel.get_x()


def get_y(pixel):
    """pixel: the pixel you want to find the y-coordinate of
       returns: the y-coordinate of the pixel
       Takes in a pixel object and returns the y position of
       where that pixel is in the picture."""

    if not pixel.__class__ == Pixel:
        raise ValueError("get_y(pixel): Input is not a pixel")
    return pixel.get_y()


##
## Global color functions ------------------------------------------------------
##


def distance(c1, c2):
    """c1: the first color you want compared
       c2: the second color you want compared
       Takes two Color objects and returns a single
       number representing the distance between the colors.
       The red, green, and blue values of the colors are
       takenas a point in (x, y, z) space, and the cartesian
       distance is computed."""

    if not c1.__class__ == Color:
        raise ValueError("distance(c1,c2): First input is not a color.")
    if not c2.__class__ == Color:
        raise ValueError("distance(c1,c2): Second input is not a color.")
    return c1.distance(c2)


def make_darker(color):
    """color: the color you want to darken
       returns: the new, darker color
       Takes a color and returns a slightly darker
       version of the original color."""

    if not color.__class__ == Color:
        raise ValueError("make_darker(color): Input is not a color.")
    color.make_darker()
    return color


def make_lighter(color):
    """color: the color you want to lighten
       returns: the new, lighter color
       Takes a color and returns a slightly lighter
       version of the original color."""

    if not color.__class__ == Color:
        raise ValueError("make_lighter(color): Input is not a color.")
    color.make_lighter()
    return color


def make_color(red, green, blue):
    """red: the amount of red you want in the color
       green: the amount of green you want in the color
       blue: the amount of blue you want in the picture
       returns: the color made from the inputs
       Takes three inputs: For the red, green, and blue
       components (in order), then returns a color object."""

    return new_color(red, green, blue)


def new_color(red, green, blue):
    """red: the amount of red you want in the color
       green: the amount of green you want in the color
       blue: the amount of blue you want in the picture
       returns: the color made from the inputs
       Takes three inputs: For the red, green, and blue
       components (in order), then returns a color object."""

    return Color(red, green, blue)


##
## DEBUG -----------------------------------------------------------------------
##

# the following allows us to wrap an error message and display specific
# information depending on the context


def exception_hook(type, value, traceback):
    try:
        global debug_level
        cur_level = debug_level
    except:
        cur_level = 0

    # handle each level

    if cur_level == 0:

        # user mode

        print str(value)
        sys.exc_clear()
    elif cur_level == 1:
        raise value
    else:

        # normal error mode

        tb = traceback
        framestack = []
        while tb:

            # get the current frame

            framestack.append(tb.tb_frame)

            # and traverse back to the top

            tb = tb.tb_next
        framestack.reverse()

        # print the message and each calling method

        print "Message: (%s)\n    %s" % (str(type), value)
        print "Stack Trace:"
        for temp_frame in framestack:
            print "    [%s:(%d)] - %s()" % (temp_frame.f_code.co_filename,
                    temp_frame.f_lineno, temp_frame.f_code.co_name)
        sys.exc_clear()


# set the hook

sys.excepthook = exception_hook

# graphical warnings and prompts


def show_warning(msg, title="Warning"):
    tkMessageBox.showwarning(title, msg)


def show_error(msg, title="Error"):
    tkMessageBox.showerror(title, msg)


#
# all prompts return:
#       -1 for cancel (if there are > 2 choices)
#       0 for no/cancel (only if there are 2 choices)
#       1 for yes/ok
#


def prompt_yes_no(prompt_msg, title):
    result = tkMessageBox.askquestion(title, prompt_msg, default=
            tkMessageBox.NO)
    if result == 'yes':
        return 1
    else:
        return 0


def prompt_ok_cancel(prompt_msg, title):
    return int(tkMessageBox.askokcancel(title, prompt_msg, default=
               tkMessageBox.CANCEL))


#
# set the default debug level
# 0 - print user friendly error msgs only (default)
# 1 - throw normal errors
# 2 - show simple errors & stack trace
#

debug_level = 0
