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
# July 27, 2007 Finished modifying the new picture.py library
#               no longer dependent on Numerical and Pygame


from Tkinter import *
import ImageFont
import os
import sys
import tkColorChooser
import tkFileDialog
import tkMessageBox
#import tkFont
import user
import thread
from color import *
from pixel import *
from pictureclass import *
from openpicturetool import *
##
## Global vars -------------------------------------------------------
##

VER = "1.3"
DEFAULT_FREQUENCY = 22050
DEFAULT_SAMPLE_SIZE = -16  # negative denotes signed number of bits
DEFAULT_NUM_CHANNELS = 1  # stereo or mono

DEFAULT_FONT = ImageFont.load_default()

MEDIA_FOLDER = user.home + os.sep

##
## Global misc functions -------------------------------------------------------
##


def open_picture_tool():
    OpenPictureTool()


def version():
    global VER
    return VER


def set_media_path():
    global MEDIA_FOLDER
    file = pick_a_folder()
    MEDIA_FOLDER = file
    print "New media folder: " + MEDIA_FOLDER


def get_media_path(filename):
    global MEDIA_FOLDER
    file = MEDIA_FOLDER + filename
    if not os.path.isfile(file):
        print "Note: There is no file at " + file
    return file


def pick_a_file(**options):
    root = Tk()
    root.title("Choose File")
    root.focus_force()
    root.geometry("0x0")
#   root.geometry("+100+200")
    if((sys.platform)[:3] == 'win'):
        root.attributes("-alpha",0.0)
    #root.withdraw()
    path = tkFileDialog.askopenfilename()

    root.destroy()
    return path

def pick_a_folder(**options):
    global MEDIA_FOLDER
    folder = tkFileDialog.askdirectory()
    if folder == '':
        folder = MEDIA_FOLDER
    return folder


def pick_a_color(**options):
    color = tkColorChooser.askcolor()
    new_color = Color(color[0][0], color[0][1], color[0][2])
    return new_color


#And for those who think of things as folders (5/14/03 AW)


def set_media_folder():
    global MEDIA_FOLDER
    file = pick_a_folder()
    MEDIA_FOLDER = file
    print "New media folder: " + MEDIA_FOLDER


def get_media_folder(filename):
    global MEDIA_FOLDER
    file = MEDIA_FOLDER + filename
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
## Global picture functions ----------------------------------------------------
##


def open_picture_tool(filename):
    """Allows you to find information about digital images.
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
        always return you to your orginal picture.
       
       filename: a string represeting the location and name of picture"""

    tool = OpenPictureTool(filename)
    if (sys.platform)[:3] == 'dar':
        tool.run_tool(True)
    else:
        p = thread.start_new_thread(tool.run_tool, (False,))

def open_picture_tool_safe(filename):
    """Allows you to find information about digital images.
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
        always return you to your orginal picture.
        
       filename: a string represeting the location and name of picture"""

    tool = OpenPictureTool(filename)
    tool.run_tool(True)
    


def make_picture(filename):
    """Creates a picture.
       
       filename: a string represeting the location and name of picture
       
       Return a instance of picture class, on success"""

    picture = Picture()
    picture.load_image(filename)
    try:
        w = picture.get_width()
        return picture
    except:
        print "Was unable to load the image in " + filename + \
            "\nMake sure it's a valid image file."

def make_empty_picture(width, height):
    """Generates a blank picture.
    
       width: the width of the picture
       height:  the height of the picture
       
       Return a instance of picture class"""

    picture = Picture()
    picture.create_image(width, height)
    return picture


def crop_picture(picture, x1, y1, x2, y2):
    """Replaces picture with a rectangular region from the current picture.
       Note coordinates are zero-based so to get a 50x50 image starting from
       top left corner the coordinates would be: 0,0,49,49.
       
       picture: the picture to be cropped
       x1: defines left pixel coordinate
       y1: defines upper pixel coordinate
       x2: defines right pixel coordinate
       y2: defines lower pixel coordinate."""

    if not picture.__class__ == Picture:
        raise ValueError("crop_picture(picture,x1,y1,x2,y2): First input is not a picture")
    picture.crop(x1, y1, x2 + 1, y2 + 1)

def set_pixels(picture, color):
    """Sets all the pixels of the picture given as first argument
       to the color given as second argument.
       
       picture: the picture to be modified
       color: the color to which all the pixels will be set"""

    if not picture.__class__ == Picture:
        raise ValueError("set_pixels(picture,color): First input is not a picture")
    if not color.__class__ == Color:
        raise ValueError("set_pixels(picture,color): Second input is not a color.")
    return picture.set_pixels(color)


def get_pixel(picture, x, y):
    """Takes a picture, an x position and a y position (two numbers),
       and returns the Pixel object at that point in the picture.
       
       picture: the picture you want to get the pixel from
       x: the x-coordinate of the pixel you want
       y: the y-coordinate of the pixel you want
       
       Return the Pixel object at the specified coordinates in the picture."""

    if not picture.__class__ == Picture:
        raise ValueError("get_pixel(picture,x,y): Input is not a picture")
    return picture.get_pixel(x, y)


def get_pixels(picture):
    '''Takes a picture as input and returns the sequence of
       Pixel objects in the picture.
       
       picture: the picture you want to get the pixels from
       
       Return a list of all the pixels in the picture'''

    if not picture.__class__ == Picture:
        raise ValueError("get_pixels(picture): Input is not a picture")
    return picture.get_pixels()


def get_width(picture):
    """Takes a picture as input and returns its length in
       the number of pixels left-to-right in the picture.
       
       picture: the picture you want to get the width of
       
       Return the width of the picture"""

    if not picture.__class__ == Picture:
        raise ValueError("get_width(picture): Input is not a picture")
    return picture.get_width()


def get_height(picture):
    """Takes a picture as input and returns its length in the
       number of pixels top-to-bottom in the picture.
       
       picture: the picture you want to get the height of
       
       Return the height of the picture"""

    if not picture.__class__ == Picture:
        raise ValueError("get_height(picture): Input is not a picture")
    return picture.get_height()


def show(picture):
    """Displays the picture. On Unix platforms, this method saves the
       image to a temporary PPM file, and calls the xv utility.
       On Windows, it saves the image to a temporary BMP file,
       and uses the standard BMP display utility to show it.
       
       picture: Picture to be displayed"""

    if not picture.__class__ == Picture:
        raise ValueError("show(picture): Input is not a picture")
    picture.show()

def add_line(picture, x1, y1, x2, y2, acolor):
    """Takes a picture, a starting (x, y) position (two numbers), and an
       ending (x, y) position (two more numbers, four total) and draws a
       line from the starting point to the ending point in the picture.
       
       picture: the picture you want to draw the line on 
       x1: the x position you want the line to start 
       y1: the y position you want the line to start
       x2: the x position you want the line to end 
       y2: the y position you want the line to end
       acolor: the color you want to draw in """

    if not picture.__class__ == Picture:
        raise ValueError("add_line(picture,x1,y1,x2,y2): Input is not a picture")
    picture.add_line(acolor, x1, y1, x2, y2)

def add_text(picture, x1, y1, string, acolor):
    """Takes a picture, an x position and a y position (two numbers),
       and some text as a string, which will get drawn into the picture,
       in the specified color.
    
       picture: the picture you want to add the text to
       x1: the x-coordinate where you want to start writing the text
       y1: the y-coordinate where you want to start writing the text
       string: s string containing the text you want written
       acolor: the color you want to draw in"""

    if not picture.__class__ == Picture:
        raise ValueError("add_text(picture,x1,y1,string): Input is not a picture")
    picture.add_text(acolor, x1, y1, string)

def add_rect(picture, x, y, w, h, acolor):
    """Takes a picture, a starting (x, y) position (two numbers), and a width
       and height (two more numbers, four total) then draws a rectangle in
       outline of the given width and height with the position (x, y) as the
       upper left corner.
       
       picture: the picture you want to draw the rectangle on
       x: the x-coordinate of the upper left-hand corner of the rectangle
       y: the y-coordinate of the upper left-hand corner of the rectangle
       w: the width of the rectangle
       h: the height of the rectangle
       acolor: the color you want to draw in"""

    if not picture.__class__ == Picture:
        raise ValueError("add_rect(picture,x,y,w,h): Input is not a picture")
    picture.add_rect(acolor, x, y, w, h)

def add_oval(picture, x, y, w, h, acolor):
    """Takes a picture, a starting (x, y) position (two numbers), and a width
       and height (two more numbers, four total) then draws an oval in
       outline of the given width and height with the position (x, y) as the
       upper left corner.
       
       picture: the picture you want to draw the oval on
       x: the x-coordinate of the upper left-hand corner of the oval
       y: the y-coordinate of the upper left-hand corner of the oval
       w: the width of the oval
       h: the height of the oval
       acolor: the color you want to draw in"""

    if not picture.__class__ == Picture:
        raise ValueError("add_oval(picture,x,y,w,h): Input is not a picture")
    picture.add_oval(acolor, x, y, w, h)

def add_rect_filled(picture, x, y, w, h, acolor):
    """Takes a picture, a starting (x, y) position (two numbers), and a width
       and height (two more numbers, four total) then draws a filled rectangle
       of the given width, height and color with the position (x, y) as the
       upper left corner.
    
       picture: the picture you want to draw the rectangle on
       x: the x-coordinate of the upper left-hand corner of the rectangle
       y: the y-coordinate of the upper left-hand corner of the rectangle
       w: the width of the rectangle
       h: the height of the rectangle
       acolor: the color you want to draw in"""

    if not picture.__class__ == Picture:
        raise ValueError("add_rect_filled(picture,x,y,w,h,acolor): Input is not a picture")
    picture.add_rect_filled(acolor, x, y, w, h)

def add_oval_filled(picture, x, y, w, h, acolor):
    """Takes a picture, a starting (x, y) position (two numbers), and a width
       and height (two more numbers, four total) then draws a filled oval
       of the given width, height and color with the position (x, y) as the
       upper left corner.
    
       picture: the picture you want to draw the oval on
       x: the x-coordinate of the upper left-hand corner of the oval
       y: the y-coordinate of the upper left-hand corner of the oval
       w: the width of the oval
       h: the height of the oval
       acolor: the color you want to draw in"""

    if not picture.__class__ == Picture:
        raise ValueError("add_rect_filled(picture,x,y,w,h,acolor): Input is not a picture")
    picture.add_oval_filled(acolor, x, y, w, h)

def add_polygon(picture, point_list, acolor):
    """Takes a picture, draws an outline (not filled) of a polygon in the
       given color with the sides being lines connecting the given vertices
    
       picture: the picture you want to draw the polygon on
       pointlist: a list containing vertices xy coordinates
                  (ex. [x1,y1,x2,y2,x3,y3])
                  It should contain at least three coordinate pairs.
       acolor: the color you want to draw in"""

    if not picture.__class__ == Picture:
        raise ValueError("add_polygon(picture,point_list,acolor): Input is not a picture")
    picture.add_polygon(acolor, point_list)

def add_polygon_filled(picture, pointlist, acolor):
    """Takes a picture, draws a filled polygon in the given color with
       the sides being lines connecting the given vertices.
    
       picture: the picture you want to draw the polygon on
       pointlist: a list containing vertices xy coordinates
                  (ex. [x1,y1,x2,y2,x3,y3])
                  It should contain at least three coordinate pairs.
       acolor: the color you want to draw in"""

    if not picture.__class__ == Picture:
        raise ValueError("add_polygon_filled(picture,pointlist,acolor): Input is not a picture")
    picture.add_polygon_filled(acolor, pointlist)


def write_picture_to(pict, filename):
    '''Takes a picture and a file name (string) as input, then writes
       the picture to the file as a JPEG. (Be sure to end the filename
       in ".jpg" for the operating system to understand it well)
    
       pict: the picture you want to be written out to a file
       path: the path to the file you want the picture written to'''

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
    """Takes in a Pixel object and a value (between 0 and 255) and sets
       the redness of that pixel to the given value.
       
       pixel: the pixel you want to set the red value in.
       value: a number (0 - 255) for the new red value of the pixel"""

    if not pixel.__class__ == Pixel:
        raise ValueError("set_red(pixel,value): Input is not a pixel")
    pixel.set_red(value)


def get_red(pixel):
    """Takes a Pixel object and returns the value (between 0 and 255)
       of the amount of redness in that pixel.
    
       pixel: the pixel you want to get the amount of red from
       
       Return the red value of the pixel"""

    if not pixel.__class__ == Pixel:
        raise ValueError("get_red(pixel): Input is not a pixel")
    return pixel.get_red()


def set_blue(pixel, value):
    """Takes in a Pixel object and a value (between 0 and 255) and sets
       the blueness of that pixel to the given value.
    
       pixel: the pixel you want to set the blue value in.
       value: a number (0 - 255) for the new blue value of the pixel"""

    if not pixel.__class__ == Pixel:
        raise ValueError("set_blue(pixel,value): Input is not a pixel")
    pixel.set_blue(value)


def get_blue(pixel):
    """Takes a Pixel object and returns the value (between 0 and 255)
       of the amount of blueness in that pixel.
    
       pixel: the pixel you want to get the amount of blue from
       
       Return the blue value of the pixel"""

    if not pixel.__class__ == Pixel:
        raise ValueError("get_blue(pixel): Input is not a pixel")
    return pixel.get_blue()


def set_green(pixel, value):
    """Takes in a Pixel object and a value (between 0 and 255) and sets
       the greeness of that pixel to the given value.
    
       pixel: the pixel you want to set the green value in.
       value: a number (0 - 255) for the new green value of the pixel"""

    if not pixel.__class__ == Pixel:
        raise ValueError("set_green(pixel,value): Input is not a pixel")
    pixel.set_green(value)


def get_green(pixel):
    """Takes a Pixel object and returns the value (between 0 and 255)
       of the amount of greenness in that pixel.
    
       pixel: the pixel you want to get the amount of green from
       
       Return the green value of the pixel"""

    if not pixel.__class__ == Pixel:
        raise ValueError("get_green(pixel): Input is not a pixel")
    return pixel.get_green()


def get_color(pixel):
    """Takes a Pixel and returns the Color object at that pixel.
    
       pixel: the pixel you want to extract the color from
       
       Return a color, the color from the pixel"""

    if not pixel.__class__ == Pixel:
        raise ValueError("get_color(pixel): Input is not a pixel")
    return pixel.get_color()


def set_color(pixel, color):
    """Takes in a pixel and a color, and sets the pixel to the provided color.
    
       pixel: the pixel you want to set the color of
       color: the color you want to set the pixel to"""

    if not pixel.__class__ == Pixel:
        raise ValueError("set_color(pixel,color): Input is not a pixel.")
    if not color.__class__ == Color:
        raise ValueError("set_color(pixel,color): Input is not a color.")
    pixel.set_color(color)


def get_x(pixel):
    """Takes in a pixel object and returns the x position of
       where that pixel is in the picture.
       
       pixel: the pixel you want to find the x-coordinate of
       
       Return the x-coordinate of the pixel"""

    if not pixel.__class__ == Pixel:
        raise ValueError("get_x(pixel): Input is not a pixel")
    return pixel.get_x()


def get_y(pixel):
    """Takes in a pixel object and returns the y position of
       where that pixel is in the picture.
    
       pixel: the pixel you want to find the y-coordinate of
       
       Return the y-coordinate of the pixel"""

    if not pixel.__class__ == Pixel:
        raise ValueError("get_y(pixel): Input is not a pixel")
    return pixel.get_y()


##
## Global color functions ------------------------------------------------------
##


def distance(c1, c2):
    """Takes two Color objects and returns a single
       number representing the distance between the colors.
       The red, green, and blue values of the colors are
       takenas a point in (x, y, z) space, and the cartesian
       distance is computed.
    
       c1: the first color you want compared
       c2: the second color you want compared
       
       Return a type float number representing the distance
       between the colors"""

    if not c1.__class__ == Color:
        raise ValueError("distance(c1,c2): First input is not a color.")
    if not c2.__class__ == Color:
        raise ValueError("distance(c1,c2): Second input is not a color.")
    return c1.distance(c2)


def make_darker(color):
    """Takes a color and returns a slightly darker
       version of the original color.
       
       color: the color you want to darken
       
       Return the new, darker color"""

    if not color.__class__ == Color:
        raise ValueError("make_darker(color): Input is not a color.")
    color.make_darker()
    return color


def make_lighter(color):
    """Takes a color and returns a slightly lighter
       version of the original color.
       
       color: the color you want to lighten
       
       Return the new, lighter color"""

    if not color.__class__ == Color:
        raise ValueError("make_lighter(color): Input is not a color.")
    color.make_lighter()
    return color

# TODO: Duplicate code? decide on make_color or new_color?

def make_color(red, green, blue):
    """Takes three inputs: For the red, green, and blue
       components (in order), then returns a color object.
       
       red: the amount of red you want in the color
       green: the amount of green you want in the color
       blue: the amount of blue you want in the picture
       
       Return the color made from the inputs"""

    return new_color(red, green, blue)


def new_color(red, green, blue):
    """Takes three inputs: For the red, green, and blue
       components (in order), then returns a color object.
    
       red: the amount of red you want in the color
       green: the amount of green you want in the color
       blue: the amount of blue you want in the picture
       
       Return the color made from the inputs"""

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