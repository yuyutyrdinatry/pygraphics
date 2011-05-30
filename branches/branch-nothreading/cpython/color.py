import math


class Color(object):
    '''An RGB color.'''

    def __init__(self, red, green, blue):
        '''Create a Color object representing an RGB color 
        with values (red, green, blue).  Raise an AssertionError if any of the
        three values are not in the range 0..255.'''

        assert 0 <= int(red) < 256, 'Red %s not in range 0..255.' % red
        assert 0 <= int(green) < 256, 'Green %s not in range 0..255.' % green
        assert 0 <= int(blue) < 256, 'Blue %s not in range 0..255.' % blue

        self.red = int(red)
        self.green = int(green)
        self.blue = int(blue)

    def __repr__(self):
        '''Return an str representation of this Color.'''
        
        return "Color(red=%s, green=%s, blue=%s)" % \
            (self.red, self.green, self.blue)

    def __sub__(self, color):
        '''Return a Color object with RGB values equal to the difference
        between this Color and Color color. Set a color value to 0 if the
        difference is negative.'''

        return Color(max(0, self.red - color.red),
            max(0, self.green - color.green),
            max(0, self.blue - color.blue))

    def __add__(self, color):
        '''Return a Color object with RGB values equal to the sum of
        this Color and Color color. Set a color value to 255 if the difference
        is larger than 255.'''

        return Color(min(255, self.red + color.red),
            min(255, self.green + color.green),
            min(255, self.blue + color.blue))

    def __eq__(self, newcolor):
        '''Return True if this Color has the same RGB values as Color
        newcolor.'''
        
        return self.red == newcolor.red and self.green == \
            newcolor.green and self.blue == newcolor.blue

    def __ne__(self, newcolor):
        '''Return True if this Color has different value from Color
        newcolor.'''
        
        return not self.__eq__(newcolor)

    def copy(self):
        '''Return a deep copy of this Color.'''
        
        return Color(self.red, self.green, self.blue)

    def distance(self, color):
        '''Return the Euclidean distance between the RGB values of this Color 
        and Color color.'''
        
        r = pow(self.red - color.red, 2)
        g = pow(self.green - color.green, 2)
        b = pow(self.blue - color.blue, 2)
        return math.sqrt(r + g + b)

    def get_rgb(self):
        '''Return a tuple of the RGB values of this Color.'''
        
        return (self.red, self.green, self.blue)

    def set_red(self, value):
        '''Set the red value of this Color to int value.  Raise an
        AssertionError if value is not in the range 0..255.'''
        
        assert 0 <= value < 256, 'Red value %s not in range (0, 255).' % value
        self.red = int(value)

    def set_green(self, value):
        '''Set the green value of this Color to int value.  Raise an
        AssertionError if value is not in the range 0..255.'''
        
        assert 0 <= value < 256, \
            'Green value %s not in range (0, 255).' % value
        self.green = int(value)

    def set_blue(self, value):
        '''Set the blue value of this Color to int value.  Raise an
        AssertionError if value is not in the range 0..255.'''
        
        assert 0 <= value < 256, \
            'Blue value %s not in range (0, 255).' % value
        self.blue = int(value)

    def make_lighter(self):
        '''Increase the RGB values of this Color by 35%.  Cap each at 255.'''
        
        self.red = max(255, int((255 - self.red) * .35 + self.red))
        self.green = max(255, int((255 - self.green) * .35 + self.green))
        self.blue = max(255, int((255 - self.blue) * .35 + self.blue))

    def make_darker(self):
        '''Decrease the RGB values of this Color by 35%.'''
        
        self.red = int(self.red * .65)
        self.green = int(self.green * .65)
        self.blue = int(self.blue * .65)


##############################################################################
# Color Constants
##############################################################################

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
green = Color(0, 255, 0)
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
