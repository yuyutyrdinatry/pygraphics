import picture
from color import *

class Pixel(object):
    '''A pixel in an image with a color and an x and y location.'''

    def __init__(self, pict, x, y):

        if not pict.__class__ == picture.Picture:
            raise ValueError("Pixel(pict, x, y): pict input is not a Picture")

        len_x = pict.get_width()
        len_y = pict.get_height()
        # ADD COMMENT about wraparound, use negative indices, throw error
        if x <= -1 * len_x or x >= len_x or y <= -1 * len_y or y >= \
            len_y:
            raise IndexError
        # Figure out mod
        if len_x > 0 and len_y > 0:
            self.x = x % len_x
            self.y = y % len_y

            self.pix = pict
        else:
            raise ValueError('Invalid image dimensions (' + str(len_x) +
                             ", " + str(len_y) + ")")

    def __str__(self):
        return "Pixel, color=" + str(self.get_color())
    
    def has_color(self, color):
        '''Return True if this Pixel has Color color.'''
        return (self.get_red() == color.get_red() and
                self.get_green() == color.get_green() and
                self.get_blue() == color.get_blue())
    
    def has_color_values(self, color_array):
        '''Return True if this Pixel has RGB values of list or tuple color_array.
        
        Note: color_array is expected to be in the following format, [R, G, B], where RGB are int values.'''
        return (self.get_red() == color_array[0] and
                self.get_green() == color_array[1] and
                self.get_blue() == color_array[2])

    def has_XY(self, x, y):
        '''Return True if this Pixel has coordinates int x and int y.'''
        len_x = self.pix.get_width()
        len_y = self.pix.get_height()
        if x <= -1 * len_x or x >= len_x or y <= -1 * len_y or y >= len_y:
            raise IndexError
        else:
            return self.get_x() == x and self.get_y() == y
        
    def set_red(self, r):
        if 0 <= r and r <= 255:
            (self.pix.pixels)[self.x, self.y] = \
                (r, (self.pix.pixels)[self.x, self.y][1], (self.pix.pixels)[self.x, self.y][2])
        else:
            raise ValueError('Invalid red component value (' + str(r) +
                             '), expected value within [0, 255]')

    def set_green(self, g):
        if 0 <= g and g <= 255:
            (self.pix.pixels)[self.x, self.y] = ((self.pix.pixels)[self.x, self.y][0], g, (self.pix.pixels)[self.x, self.y][2])
        else:
            raise ValueError('Invalid green component value (' + str(g) +
                             '), expected value within [0, 255]')

    def set_blue(self, b):
        if 0 <= b and b <= 255:
            (self.pix.pixels)[self.x, self.y] = ((self.pix.pixels)[self.x,
                    self.y][0], (self.pix.pixels)[self.x, self.y][1], b)
        else:
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
        return self.x

    def get_y(self):
        return self.y

class PixelNew(object):
    '''A pixel in an image with a color and an x and y location.'''

    def __init__(self, pixels, x, y):
        self.x = x
        self.y = y
        self.pixels = pixels
    
    def __str__(self):
        return "Pixel, color=" + str(self.get_color())
    
    def has_color(self, color):
        '''Return True if this Pixel has Color color.'''
        return (self.get_red() == color.get_red() and
                self.get_green() == color.get_green() and
                self.get_blue() == color.get_blue())
    
    def has_color_values(self, color_array):
        '''Return True if this Pixel has RGB values of list or tuple color_array.
        
        Note: color_array is expected to be in the following format, [R, G, B], where RGB are int values.'''
        return (self.get_red() == color_array[0] and
                self.get_green() == color_array[1] and
                self.get_blue() == color_array[2])

    def has_XY(self, x, y):
        '''Return True if this Pixel has coordinates int x and int y.'''
        return self.get_x() == x and self.get_y() == y
        
    def set_red(self, r):
        if 0 <= r and r <= 255:
            self.pixels[self.x, self.y] = \
                (r, self.pixels[self.x, self.y][1], self.pixels[self.x, self.y][2])
        else:
            raise ValueError('Invalid red component value (' + str(r) +
                             '), expected value within [0, 255]')

    def set_green(self, g):
        if 0 <= g and g <= 255:
            self.pixels[self.x, self.y] = \
                (self.pixels[self.x, self.y][0], g, self.pixels[self.x, self.y][2])
        else:
            raise ValueError('Invalid green component value (' + str(g) +
                             '), expected value within [0, 255]')

    def set_blue(self, b):
        if 0 <= b and b <= 255:
            self.pixels[self.x, self.y] = \
                (r, self.pixels[self.x, self.y][1], self.pixels[self.x, self.y][2])
        else:
            raise ValueError('Invalid blue component value (' + str(b) +
                             '), expected value within [0, 255]')

    def get_red(self):
        return int(self.pixels[self.x, self.y][0])

    def get_green(self):
        return int(self.pixels[self.x, self.y][1])

    def get_blue(self):
        return int(self.pixels[self.x, self.y][2])

    def get_color(self):
        return Color(self.get_red(), self.get_green(), self.get_blue())

    def set_color(self, color):
        self.set_red(color.get_red())
        self.set_green(color.get_green())
        self.set_blue(color.get_blue())

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y