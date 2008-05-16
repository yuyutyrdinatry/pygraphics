from color import *

class Pixel(object):
    '''A pixel in an image with a color and an x and y location.'''

    def __init__(self, pixels, x, y):
        '''Constructor for the Pixel class.
        
        Requires:
        - PIL PixelAccess object "pixels"
        - in-bounds int coordinates x and y'''
        self.x = x
        self.y = y
        # This is a PixelAccess object implemented in C
        # It is a two-dimensional array (e.g. PixelAccess[x, y])
        # used to access color tuples.
        self.pixels = pixels
    
    def __str__(self):
        '''Return a str with color information for this Pixel'''
        return "Pixel, color=" + str(self.get_color())
   
    def __repr__(self):
        '''Return a str representation of this Pixel'''
        return "Pixel(%d, %d, %s)" % (self.x, self.y,
                                            repr(self.get_color()))

    def has_color(self, color):
        '''Return True if this Pixel has Color color.'''
        return (self.get_red() == color.get_red() and
                self.get_green() == color.get_green() and
                self.get_blue() == color.get_blue())
    
    def has_color_values(self, color_array):
        '''Return True if this Pixel has RGB values of list color_array.
        
        Note: color_array is expected to be in the following format, [R, G, B], 
        where RGB are int values.'''
        return (self.get_red() == color_array[0] and
                self.get_green() == color_array[1] and
                self.get_blue() == color_array[2])

    def has_XY(self, x, y):
        '''Return True if this Pixel has coordinates int x and int y.'''
        return self.get_x() == x and self.get_y() == y
        
    def set_red(self, r):
        '''Set red value of this Pixel to int r. Raise ValueError if r is not
        a valid color value [0, 256]'''
        if 0 <= r and r <= 255:
            self.pixels[self.x, self.y] = \
                (r, self.pixels[self.x, self.y][1], self.pixels[self.x, self.y][2])
        else:
            raise ValueError('Invalid red component value (' + str(r) +
                             '), expected value within [0, 255]')

    def set_green(self, g):
        '''Set green value of this Pixel to int g. Raise ValueError if g is not
        a valid color value [0, 256]'''
        if 0 <= g and g <= 255:
            self.pixels[self.x, self.y] = \
                (self.pixels[self.x, self.y][0], g, self.pixels[self.x, self.y][2])
        else:
            raise ValueError('Invalid green component value (' + str(g) +
                             '), expected value within [0, 255]')

    def set_blue(self, b):
        '''Set blue value of this Pixel to int b. Raise ValueError if b is not
        a valid color value [0, 256]'''
        if 0 <= b and b <= 255:
            self.pixels[self.x, self.y] = \
                (self.pixels[self.x, self.y][0], self.pixels[self.x, self.y][1], b)
        else:
            raise ValueError('Invalid blue component value (' + str(b) +
                             '), expected value within [0, 255]')

    def get_red(self):
        '''Return the red value of this Pixel.'''
        return int(self.pixels[self.x, self.y][0])

    def get_green(self):
        '''Return the green value of this Pixel.'''
        return int(self.pixels[self.x, self.y][1])

    def get_blue(self):
        '''Return the blue value of this Pixel.'''
        return int(self.pixels[self.x, self.y][2])

    def get_color(self):
        '''Return a Color object representing the color of this Pixel.'''
        return Color(self.get_red(), self.get_green(), self.get_blue())

    def set_color(self, color):
        '''Set the color values of this Pixel to those of Color object color.'''
        self.set_red(color.get_red())
        self.set_green(color.get_green())
        self.set_blue(color.get_blue())

    def get_x(self):
        '''Return the x value of this Pixel.'''
        return self.x

    def get_y(self):
        '''Return the y value of this Pixel.'''
        return self.y
    
if __name__ == '__main__':
    from picture import *
    pic = Picture(10,10)
    p = pic.get_pixel(1,1)
    print repr(p)