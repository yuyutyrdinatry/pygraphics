from color import *
from picture import *
from pixel import *
import wx
import os

IMAGE_FORMATS = ['*.jpg', '*.bmp', '*.gif']
##
## Global picture functions ---------------------------------------------------
##


def load_picture(filename):
    '''Return a Picture object from filename filename.'''

    return Picture(filename=filename)


def create_picture(w, h, col=white):
    '''Return a Picture w pixels wide and h pixels high. 
    Default Color col is white.'''
    
    return Picture(w, h, col)


def crop(pic, x1, y1, x2, y2):
    '''Crop Picture pic so that only pixels inside the rectangular region 
    with upper-left coordinates (x1, y1) and lower-right coordinates (x2, y2) 
    remain.  The new upper-left coordinate is (0, 0).'''
            
    pic.crop(x1, y1, x2, y2)


def get_pixel(pic, x, y):
    '''Return the Pixel object at the coordinates (x, y) in Picture pic.'''
    
    return pic.get_pixel(x, y)


def get_pixels(pic):
    '''Return a list of Picture pic's Pixels from left to right, 
    top row to bottom row.'''

    return [pixel for pixel in pic]


def get_width(pic):
    '''Return how many pixels wide Picture pic is.'''
    
    return pic.get_width()


def get_height(pic):
    '''Return how many pixels high Picture pic is.'''
    
    return pic.get_height()


def show(pic):
    '''Display Picture pic in separate window.'''
    
    pic.show()


def add_line(pic, x1, y1, x2, y2, col):
    '''Draw a line of Color col from (x1, y1) to (x2, y2) on Picture pic.'''
    
    pic.add_line(col, x1, y1, x2, y2)


def add_text(pic, x, y, s, col):
    '''Draw str s in Color col on Picture pic starting at (x, y).'''
    
    pic.add_text(col, x, y, s)


def add_rect(pic, x, y, w, h, col):
    '''Draw an empty rectangle of Color col, width w, and height h 
    on Picture pic. The upper left corner of the rectangle is at (x, y).'''
    
    pic.add_rect(col, x, y, w, h)


def add_rect_filled(pic, x, y, w, h, col):
    '''Draw a filled rectangle of Color col, width w, and height h 
    on Picture pic. The upper left corner of the rectangle is at (x, y).'''
    
    pic.add_rect_filled(col, x, y, w, h)


def add_oval(pic, x, y, w, h, col):
    '''Draw an empty oval of Color col, width w, and height h on Picture pic.
    The upper left corner of the oval is at (x, y).'''
    
    pic.add_oval(col, x, y, w, h)


def add_oval_filled(pic, x, y, w, h, col):
    '''Draw a filled oval of Color col, width w, and height h on Picture pic.
    The upper left corner of the oval is at (x, y).'''
    
    pic.add_oval_filled(col, x, y, w, h)


def add_polygon(pic, point_list, col):
    '''Draw an empty polygon of Color col with corners for every vertex 
    in list point_list on Picture pic.
    
    Note:
    point_list is a list containing vertices xy coordinates 
    (ex. [x1,y1,x2,y2,x3,y3]) It should contain at least 
    three coordinate pairs.'''
    
    pic.add_polygon(col, point_list)


def add_polygon_filled(pic, point_list, col):
    '''Draw an empty polygon of Color col with corners for every vertex 
    in list point_list on Picture pic.
    
    Note:
    point_list is a list containing vertices xy coordinates 
    (ex. [x1,y1,x2,y2,x3,y3]) It should contain at least 
    three coordinate pairs.'''
    
    pic.add_polygon_filled(col, point_list)


def save_as(pic):
    '''Prompt user to pick a directory and filename then write Picture pic
    to that filename. Requires that file format is specified in filename 
    by extensions (e.g. ".jpg", ".gif", ".bmp").'''
    
    filename = choose_save_location()
    pic.save_as(filename)

    
def save(pic):
    '''Write Picture pic back to its previous file.'''
    
    if pic.get_filename() == '':
        save_as(pic)
    else:
        pic.save()


##
## Global pixel functions ------------------------------------------------------
##


def set_red(pix, r):
    '''Set the red value of Pixel pix to r.'''
    
    pix.set_red(r)


def get_red(pix):
    '''Return the red value of Pixel pix.'''
    
    return pix.get_red()


def set_blue(pix, b):
    '''Set the blue value of Pixel pix to b.'''

    pix.set_blue(b)


def get_blue(pix):
    '''Return the blue value of Pixel pix.'''
    
    return pix.get_blue()


def set_green(pix, g):
    '''Set the green value of Pixel pix to g.'''

    pix.set_green(g)


def get_green(pix):
    '''Return the green value of Pixel pix.'''
    
    return pix.get_green()


def get_color(pix):
    '''Return the Color object with Pixel pix's RGB values.'''
    
    return pix.get_color()


def set_color(pix, col):
    '''Set the RGB values of Pixel pix to those of Color col.'''

    pix.set_color(col)


def get_x(pix):
    '''Return the x coordinate of Pixel pix.'''
    
    return pix.get_x()


def get_y(pix):
    '''Return the y coordinate of Pixel pix.'''
    
    return pix.get_y()


##
## Global color functions ------------------------------------------------------
##


def distance(col1, col2):
    '''Return the Euclidean distance between the RGB values of Color col1 and
    Color col2.'''
    
    return col1.distance(col2)


def darken(col):
    '''Darken Color col by 35%.'''
    
    col.make_darker()


def lighten(col):
    '''Lighten Color col by 35%.'''
    
    col.make_lighter()


def create_color(r, g, b):
    '''Return a Color object with RGB values r, g, and b.'''
    
    return Color(r, g, b)

##
## Media functions -------------------------------------------------------
##


def inspect(obj):
    '''Inspect object obj. Works on most top level media.py objects.'''
    
    obj.inspect()


def copy(obj):
    '''Return a deep copy of object obj. Works on most media.py objects.'''
    
    return obj.copy()


def choose_save_filename():
    '''Prompt user to pick a directory and filename. Return the path
    to the new file. Change the current working directory to the directory 
    where the file chosen by the user is.'''
    
    app = wx.App()
       
    formats = get_formats()
    dlg = wx.FileDialog(None, message="Choose a filename:", 
                        defaultDir=os.getcwd(), wildcard=formats, style=wx.SAVE)
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
        os.chdir(os.path.dirname(path))
        return path
    dlg.Destroy()


def choose_file():
    '''Prompt user to pick a file. Return the path to that file. 
    Change the current working directory to the directory 
    where the file chosen by the user is'''
    
    app = wx.App()
         
    dlg = wx.FileDialog(None, message="Choose a file:", defaultDir=os.getcwd(),
                        style=wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
        os.chdir(os.path.dirname(path))
        return path
    dlg.Destroy()

def choose_folder():
    '''Prompt user to pick a folder. Return the path to that folder. 
    Change the current working directory to the directory where the folder
    chosen by the user is.'''
   
    app = wx.App()

    dlg = wx.DirDialog(None, title="Choose a directory:", 
                       defaultPath=os.getcwd())
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
        os.chdir(os.path.dirname(path))
        return path
    dlg.Destroy()

def choose_color():
    '''Prompt user to pick a color. Return a RGB Color object.'''
    
    app = wx.App()
     
    dlg = wx.ColourDialog(None)
    dlg.GetColourData().SetChooseFull(True)
    if dlg.ShowModal() == wx.ID_OK:
        data = dlg.GetColourData().GetColour().Get()
        return Color(data[0], data[1], data[2])
    dlg.Destroy()
    
def get_formats():
    '''Return a string from the global variable IMAGE_FORMATS.
    
    This string is usable by the wxPython wxFileDialog object to specify
    the available file formats.'''
    
    formats = ''
    for format in IMAGE_FORMATS:
        format = format[-3:].upper() + ' file (' + format + ')|' + format + '|'
        formats += format
    
    return formats[:-1]

if __name__ == '__main__':
    print choose_file()