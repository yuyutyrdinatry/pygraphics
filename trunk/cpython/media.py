import numpy
import os
import pygame
import wx
import  wx.lib.imagebrowser    as  ib

IMAGE_FORMATS = ['*.jpg', '*.bmp', '*.gif']
AUDIO_FORMATS = ['*.wav']

DEFAULT_FREQUENCY = 22050
DEFAULT_ENCODING = -16
DEFAULT_CHANNELS = 2
DEFAULT_BUFFERING = 2048
pygame.mixer.pre_init(DEFAULT_FREQUENCY, 
                      DEFAULT_ENCODING, 
                      DEFAULT_CHANNELS, 
                      DEFAULT_BUFFERING)
pygame.mixer.init()

from color import *
from picture import *
from pixel import *
from sample import *
from sound import *

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
## Global sound functions ------------------------------------------------------
##


def load_sound(filename):    

    return Sound(filename=filename)


def create_empty_sound(sec):

    return Sound(seconds=sec)


def get_samples(snd):

    return [samp for samp in snd]


def play(snd):

    snd.play()


def play_in_range(snd, first, last):

    snd.play(first, last)


def stop(snd):
    
    snd.stop()
    
    
def get_sampling_rate(snd):

    return snd.get_sampling_rate()


def set_sampling_rate(snd, freq):

    return snd.set_sampling_rate(freq)


def get_sample(snd, i):

    return snd.get_sample(i)


##
## Global sample functions -----------------------------------------------------
##


def set_value(samp,value):

    return samp.set_value(value)


def get_value(samp):

    return samp.get_value()


##
## Global sound graphing functions ---------------------------------------------
##

# This function plots the sound graph.
# By default the size of the graph is 1024x300
# TODO: Make it zoom capable
def plot_waveform(snd, width=1024, height=300):
   
    win = Toplevel()

    c = tkSnack.SnackCanvas(win, background="#060", width=width, height=height)
    c.pack()
    c.create_waveform(0, 0, fill="#0f0" , sound=snd.tk_sound, width=width, height=height, zerolevel=1)
    

def plot_spectrogram(snd, width=1024, height=300):

    win = Toplevel()

    c = tkSnack.SnackCanvas(win, background="#060", width=width, height=height)
    c.pack()
    c.create_spectrogram(0, 0, sound=snd.tk_sound, width=width, height=height)


def plot_spectrum(snd, width=1024, height=300):
    
    win = Toplevel()

    c = tkSnack.SnackCanvas(win, background="#060",width=width, height=height)
    c.pack()
    c.create_section(0, 0, fill="#0f0", sound=snd.tk_sound, width=width, height=height)


##
## Media functions -------------------------------------------------------
##


def save_as(obj, filename=None):
    '''Prompt user to pick a directory and filename then write media.py object
    obj to that filename. Requires that file format is specified in filename
    by extensions.'''
    
    if not filename:
        filename = choose_save_filename()

    if filename:
        obj.save_as(filename)

    
def save(obj):
    '''Write media.py object obj back to its previous file.'''
    
    if obj.get_filename() == '':
        save_as(obj)
    else:
        obj.save()


def inspect(obj):
    '''Inspect object obj. Works on most media.py objects.'''
    
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
    Change the current working directory to the directory chosen by the user.'''
   
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
    
    This string is usable by the wxFileDialog object to specify
    the available file formats.'''
    
    formats = ''
    for format in IMAGE_FORMATS:
        format = format[-3:].upper() + ' files (' + format + ')|' + format + '|'
        formats += format
    for format in AUDIO_FORMATS:
        format = format[-3:].upper() + ' files (' + format + ')|' + format + '|'
        formats += format
    
    return formats[:-1]


def ask(s, num=False, hidden=False, choices=None, multi=False):
    '''Display a dialog containing s, a text field for a response, and an "OK"
    and "CANCEL" button. The optional parameters modify the look of the dialog
    in listed priority: 
        If the optional bool num is given as True, the dialog will contain
    a numerical input slider. Return an int of the input.
        If the optional bool hidden is given as True, the entry box will show
    all text given in a manner similar to a password box. Return a str of the
    input.
        If the optional list choices is given which is a list of strings, the 
    dialog box will show a selection box from where the user may choose one 
    of the given options. Return an int indicating the index of the chosen
    option in choices. If the bool multi is given as True, the user may choose
    multiple options from the given choices. Will return a list of ints
    indicating the indices of the selected options from the given choices.'''

    app = wx.App()
    
    # Ignore all other parameters, will only show a number entry box!
    if ( num is not False ):
        dlg, get_bind = _ask_num(s)
    
    # Now we want a password input box, all other parameters ignored.
    elif ( hidden is not False ):
        dlg, get_bind = _ask_hidden(s)
        
    # Choices have been specified, so show a selection dialog
    elif ( choices is not None ):
        dlg, get_bind = _ask_multi(s, choices, multi)
    
    # Default behaviour, simple text entry dialog
    else:
        dlg, get_bind = _ask_default(s)
        
    if ( dlg.ShowModal() == wx.ID_OK ):
        dlg.Destroy()
        return get_bind()

def _ask_num(s):
    '''Given a str s, show a wxNumberEntryDialog with the given text. The user
    may input a number between [0, 2**30] inclusive. Return a tuple of the
    open dialog box and the method which can be used to retrieve the data from
    the dialog box. Assumes a wxApp is already open.'''
    
    dlg = wx.NumberEntryDialog(None, s, prompt="Input:", 
                               caption="Please enter a number...", value=0,
                               min=0, max=2**30)
    get_bind = dlg.GetValue
    return (dlg, get_bind)

def _ask_hidden(s):
    '''Given a str s, show a wxPasswordEntryDialog with the given text. The user
    may input any string. Return a tuple of the open dialog box and the method 
    which can be used to retrieve the data from the dialog box. Assumes a wxApp
    is already open.'''
    
    dlg = wx.PasswordEntryDialog(None, s, caption="Please input data...")
    get_bind = dlg.GetValue
    return (dlg, get_bind)

def _ask_multi(s, choices, multi=False):
    '''Given a str s, and a list of strs choices, show a wxSingleChoiceDialog
    with the given text s. If the optional boolean multi is True, then show a
    wxMultiChoiceDialog instead. The open dialog will be populated by the
    options given in choices. Return a tuple of the open dialog box and the 
    method which can be used to retrieve the data from the dialog box. Assumes a
    wxApp is already open.'''
    
    if ( multi is False ):
        dlg = wx.SingleChoiceDialog(None, s, "Please choose an option...",
                                    choices)
        get_bind = dlg.GetSelection
    else:
        dlg = wx.MultiChoiceDialog(None, s, 
                                   "Please choose one or more options...",
                                   choices)
        get_bind = dlg.GetSelections
    return (dlg, get_bind)

def _ask_default(s):
    '''Given a str s, show a wxTextEntryDialog with the given text. The user may
    input any string. Return a tuple of the open dialog box and the method which
    can be used to retrieve the data from the dialog box. Assumes a wxApp is 
    already open.'''
    
    dlg = wx.TextEntryDialog(None, s, "Please input data...")
    get_bind = dlg.GetValue
    return (dlg, get_bind)

def say(s):
    '''Display a dialog containing s and an "OK" button.'''
    
    app = wx.App()
    
    dlg = wx.MessageDialog(None, s, caption='Message for you!', 
                           style=wx.OK|wx.ICON_INFORMATION|wx.STAY_ON_TOP)
    dlg.ShowModal()
    dlg.Destroy()

def browse(dir=None):
    '''Display an image browser for directory dir, or the current directory if
    dir is None.'''
    
    app = wx.App()
    #panel = wx.Panel(app, -1)
    
    # set the initial directory for the demo bitmaps
    initial_dir = os.getcwd()

    # open the image browser dialog
    dlg = ib.ImageDialog(None, initial_dir)

    dlg.Centre()
    if dlg.ShowModal() == wx.ID_OK:
        # show the selected file
        say("You Selected File: " + dlg.GetFile())        
    else:
        say("You pressed Cancel\n")

    dlg.Destroy()

if __name__ == '__main__':
    L = []
    L.append(browse())
    # L.append(say('this is a say box'))
    # L.append(ask('plain old default ask box'))
    # L.append(ask('we want a number', num=True))
    # L.append(ask('passwords for all! :o', hidden=True))
    # L.append(ask('so many choices...', choices=['choice 1', 'choice 2', 'choice 3']))
    # L.append(ask('so little time...', choices=['oh', 'my', 'gawd'], multi=True))
    print L
    
#    s = load_sound('/work/songsparrow.wav')
#    s.play()
