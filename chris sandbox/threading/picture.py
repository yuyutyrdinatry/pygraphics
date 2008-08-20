'''The Picture class and helper functions. This currently supports the
following formats: JPEG, BMP, GIF, TIFF, IM, MSP, PNG, PCX, and PPM.'''

from color import *
from pixel import *
import Image
import ImageDraw
import ImageFont
import ImageTk
import os
import show_window as show_window
import mediawindows as mediawindows
import graphics

DEFAULT_FONT = ImageFont.load_default()
IMAGE_FORMATS = ['.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff', '.im', \
                  '.msp', '.png', '.pcx', '.ppm']

class Picture(object):
    '''A Picture class as a wrapper for PIL's Image class.'''
    
    
    def __init__(self, w=None, h=None, col=white, image=None, filename=None):
        '''Create a Picture object.
        
        Requires one of:
        - ints w, h, and Color col, e.g. Picture(100, 100, Color(0, 0, 0))
        - named PIL RGB Image argument image, e.g. Picture(image=Image)
        - named str argument filename, e.g. Picture(filename='image.jpg').'''
        
        self.set_filename_and_title(filename)
        self.win = None
        self.showim = None
        
        if image != None:
            image = image
        elif filename != None:
            
            # This raises an IOError if filename is not a path
            # to a file or a valid image file.
            image = load_image(filename)
        elif w != None and h != None:
            if w > 0 and h > 0:
                image = create_image(w, h, col)
            else:
                raise ValueError('Invalid width/height specified.')
        else:
            raise TypeError("No arguments were given to the Picture constructor.")
        
        self.set_image(image)
        
        self.show_window = None
        self.poll_thread = None

    
    def __str__(self):
        '''Return a str of this Picture with its filename, width, and height.'''
        
        return "Picture, filename=" + self.filename + " height=" + \
            str(self.get_height()) + " width=" + str(self.get_width())

    
    def __iter__(self):
        '''Return this Picture's Pixels from left to right,
        top row to bottom row.'''
        
        for x in xrange(0, self.get_width()):
            for y in xrange(0, self.get_height()):
                yield Pixel(self.pixels, x, y)

    
    def has_coordinates(self, x, y):
        '''Return True if (x, y) is a valid coordinate for this Picture.'''
        
        return 0 <= x < self.get_width() and 0 <= y < self.get_height()
    
    
    def set_image(self, image):
        '''Set the PIL RGB Image image in this Picture and load
        the PixelAccess object from the Image.'''
        
        if image.__class__ != Image.Image:
            raise ValueError("set_image takes a PIL Image as an argument. "
                             + repr(image) + " is not a PIL Image.")
        self.image = image
        
        # Load pixels 2D array from the Image
        self.pixels = image.load()

    
    def get_image(self):
        '''Return this Picture's PIL Image object.'''
        
        return self.image
    
    
    def copy(self):
        '''Return a deep copy of this Picture.'''
        
        pic = Picture(image=self.image.copy())
        pic.set_filename_and_title(self.filename)
        return pic
    
    
    def _make_window(self, x, y):
        
        title = 'File: %s' % self.get_filename()
        self.win = graphics.PictureWindow(title=title, width=x, height=y)
        self.win.setCoords(0, y - 1, x - 1, 0)
    
    
    def _draw_image_to_win(self, win):
        
        width = win.getWidth()
        height = win.getHeight()
        self.showim = graphics.WindowImage(graphics.WindowPoint(width/2, height/2), ImageTk.PhotoImage(self.get_image()))
        self.showim.draw(win)
        

    def show(self):
        
        if self.win:
            self.win.close()
        width = self.get_width()
        height = self.get_height()
        self._make_window(width, height + 20)
        self._draw_image_to_win(self.win)
        
    def update(self):
        
        if self.win and self.showim:
            width = self.get_width()
            height = self.get_height()
            self.showim.undraw()
            self._draw_image_to_win(self.win)
    
    def inspect(self):
        '''Inspect this Picture in an OpenPictureTool.'''
        
        tool = mediawindows.PictureInspector(self)
        tool.run_window()

    
    def get_pixel(self, x, y):
        '''Return the Pixel at coordinates (x, y).'''
        
        return Pixel(self.pixels, x, y)

    
    def set_title(self, title):
        '''Set title of this Picture to str title.'''
        
        self.title = title
        
    
    def set_filename_and_title(self, filename):
        '''If filename is a file set the filename and title of this Picture.
        Otherwise set both to the empty string.'''
        
        if filename and os.path.isfile(filename):
            self.filename = str(filename)
            self.title = get_short_path(filename)
        else:
            self.filename = ''
            self.title = ''
    
    
    def get_filename(self):
        '''Return this Picture's filename.'''
        
        return self.filename
    
    
    def get_title(self):
        '''Return this Picture's title.'''
        
        return self.title
    
    
    def get_width(self):
        '''Return how many pixels wide this Picture is.'''
        
        return self.image.size[0]
    
    
    def get_height(self):
        '''Return how many pixels high this Picture is.'''
        
        return self.image.size[1]
        
    
    def crop(self, x1, y1, x2, y2):
        '''Crop Picture pic so that only pixels inside the rectangular region
        with upper-left coordinates (x1, y1) and lower-right coordinates
        (x2, y2) remain. The new upper-left coordinate is (0, 0).'''
        
        # Check for invalid dimensions
        if not self.has_coordinates(x1, y1) or not self.has_coordinates(x2, y2)\
        or x1 > x2 or y1 > y2:
            raise IndexError('Invalid coordinates specified.')
        
        # Crop is not inclusive of the last pixel
        corners = (x1, y1, x2 + 1, y2 + 1)
        
        temp = self.image.crop(corners)
        new = temp.copy()
        self.set_image(new)
            
    
    def add_rect_filled(self, col, x, y, w, h):
        '''Draw a filled rectangle of Color col, width w, and height h
        on this Picture. The upper left corner of the rectangle is at (x, y).'''
        
        if not self.has_coordinates(x, y):
            raise IndexError("Invalid coordinates specified.")
        if w < 0 and h < 0:
            raise ValueError('Invalid width/height specified.')
        draw = ImageDraw.Draw(self.image)
        draw.rectangle([x, y, x + w, y + h], outline=tuple(col.get_rgb()),
                       fill=tuple(col.get_rgb()))
    
    
    def add_rect(self, col, x, y, w, h):
        '''Draw an empty rectangle of Color col, width w, and height h
        on this Picture. The upper left corner of the rectangle is at (x, y).'''
        
        if not self.has_coordinates(x, y):
            raise IndexError("Invalid coordinates specified.")
        if w < 0 and h < 0:
            raise ValueError('Invalid width/height specified.')
        draw = ImageDraw.Draw(self.image)
        draw.rectangle([x, y, x + w, y + h], outline=tuple(col.get_rgb()))
    
    
    def add_polygon(self, col, point_list):
        '''Draw an empty polygon of Color col with corners for every vertex
        in list point_list on this Picture.
        
        Note:
        point_list is a list containing vertices xy coordinates
        (ex. [x1,y1,x2,y2,x3,y3]) It should contain at least
        three coordinate pairs.'''
        
        i = 0
        while i < len(point_list):
            if not self.has_coordinates(point_list[i], point_list[i + 1]):
                raise IndexError("Invalid coordinates specified.")
            i += 2
        draw = ImageDraw.Draw(self.image)
        draw.polygon(point_list, outline=tuple(col.get_rgb()))
    
    
    def add_polygon_filled(self, col, point_list):
        '''Draw a filled polygon of Color col with corners for every vertex
        in list point_list on this Picture.
        
        Note:
        point_list is a list containing vertices xy coordinates
        (ex. [x1,y1,x2,y2,x3,y3]) It should contain at least
        three coordinate pairs.'''
        
        i = 0
        while i < len(point_list):
            if not self.has_coordinates(point_list[i], point_list[i + 1]):
                raise IndexError("Invalid coordinates specified.")
            i += 2
        draw = ImageDraw.Draw(self.image)
        draw.polygon(point_list, outline=tuple(col.get_rgb()), fill=
                     tuple(col.get_rgb()))
    
    
    def add_oval_filled(self, col, x, y, w, h):
        '''Draw a filled oval of Color col, width w, and height h
        on this Picture. The upper left corner of the oval is at (x, y).'''
        
        if not self.has_coordinates(x, y):
            raise IndexError("Invalid coordinates specified.")
        if w < 0 and h < 0:
            raise ValueError('Invalid width/height specified.')
        draw = ImageDraw.Draw(self.image)
        draw.ellipse([x, y, x + w, y + h], outline=tuple(col.get_rgb()),
                     fill=tuple(col.get_rgb()))
        
    
    def add_oval(self, col, x, y, w, h):
        '''Draw an empty oval of Color col, width w, and height h
        on this Picture. The upper left corner of the oval is at (x, y).'''
        
        if not self.has_coordinates(x, y):
            raise IndexError("Invalid coordinates specified.")
        if w < 0 and h < 0:
            raise ValueError('Invalid width/height specified.')
        draw = ImageDraw.Draw(self.image)
        draw.ellipse([x, y, x + w, y + h], outline=tuple(col.get_rgb()))
        
    
    def add_line(self, col, x1, y1, x2, y2, width=1):
        '''Draw a line of Color col and width width from (x1, y1) to (x2, y2)
        on this Picture.'''
        
        if not self.has_coordinates(x1, y1) or not self.has_coordinates(x2, y2):
            raise IndexError("Invalid coordinates specified.")
        draw = ImageDraw.Draw(self.image)
        draw.line([x1, y1, x2, y2], fill=tuple(col.get_rgb()), width=
                  width)
    
    
    def add_text(self, col, x, y, s):
        '''Draw str s in Color col on this Picture starting at (x, y).'''
        
        if not self.has_coordinates(x, y):
            raise IndexError("Invalid coordinates specified.")
        global DEFAULT_FONT
        self.add_text_with_style(col, x, y, s, DEFAULT_FONT)
    
    
    def add_text_with_style(self, col, x, y, s, font):
        '''Draw str s in Color col and font font on this Picture
        starting at (x, y).'''
        
        if not self.has_coordinates(x, y):
            raise IndexError("Invalid coordinates specified.")
        draw = ImageDraw.Draw(self.image)
        draw.text((x, y), text=s, fill=tuple(col.get_rgb()),
                  font=font)
        
    
    def save(self):
        '''Write this Picture back to its file. If an extension is not
        specified the default is .bmp.'''
        
        filename = os.path.splitext(self.filename)[0]
        ext = os.path.splitext(self.filename)[-1]
        if ext == '':
            self.image.save(filename + '.bmp')
        else:
            self.save_as(self.filename)
    
    def save_as(self, filename):
        '''Write this Picture to filename filename and re-set filename and
        title. Make sure to specify the file format by the extension.'''
        
        ext = os.path.splitext(filename)[-1]
        if ext in IMAGE_FORMATS or ext in [e.upper() for e in IMAGE_FORMATS]:
            self.image.save(filename)
            self.set_filename_and_title(filename)
        else:
            raise ValueError("%s is not one of the supported file formats." \
                             % ext)


##
## Helper functions ---------------------------------------------------
##


def load_image(f):
    '''Return a new PIL RGB Image object loaded from filename f.'''
    
    return Image.open(f).convert("RGB")


def create_image(w, h, col=white):
    '''Return a new PIL RGB Image object of Color col,
    w pixels wide, and h pixels high.'''
    
    return Image.new("RGB", (w, h), color=col.get_rgb())


def get_short_path(filename):
    '''Return the short path (containing directory and filename)
    of str filename.'''
    
    dirs = filename.split(os.sep)
    if len(dirs) < 1:  # does split() ever get to this stage?
        return "."
    elif len(dirs) == 1:
        return dirs[0]
    else:
        return dirs[len(dirs) - 2] + os.sep + dirs[len(dirs) - 1]
        

if __name__ == '__main__':
    a = Picture(filename='/Users/pgries/img1.jpg')
    
    b = Picture(200,300,green)
    c = Picture(500,500,red)
    b.show()
