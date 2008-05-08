import Image
import ImageDraw
import os
import pixel
from color import *

class Picture(object):

    def __init__(self, auto_repaint=False):
        self.title = "Unnamed"
        self.surf = None
        self.win_active = 0

    def __initialize_picture(self, surf, filename, title):
        self.surf = surf

        # we get the pixels array from the surface

        self.pixels = surf.load()

        self.filename = filename
        self.title = title

    def create_image(self, width, height):

        # fail if dimensions are invalid

        if width <= 0 or height <= 0:
            raise ValueError("create_image(" + str(width) + ", " + str(height) +
                             "): Invalid image dimensions")
        else:
            self.__initialize_picture(Image.new("RGB", (width, height)),
                    '', 'None')

    def load_image(self, filename):
        # global media_folder
        # if not os.path.isabs(filename):
        #    filename = media_folder + filename

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

    def crop(self, x1, y1, x2, y2):
        maxX = self.get_width()
        None
        maxY = self.get_height()
        None
        if not 0 <= x1 <= maxX or not 0 <= y1 <= maxY or not x1 < x2 <= \
            maxX or not y1 < y2 <= maxY:
            raise ValueError('Invalid width/height specified')

        image = self.surf.crop((x1, y1, x2, y2))
        self.__initialize_picture(image, self.filename, self.title)

    def clear(self, color=black):

        # clears the picture pixels to black

        self.set_pixels(color)

    def __str__(self):
        return "Picture, filename " + self.filename + " height " + str(self.get_height()) + \
            " width " + str(self.get_width())

    def show(self):
        #if (sys.platform)[:3] == 'win':
        #    i = 1
        #    p = thread.start_new(self.showchild, (i, ))
        #    time.sleep(0.1)
        #else:
        self.surf.show()

        #if raw_input() == 'c': pass

    def showchild(self, tid):
        self.surf.show()

    def do_pick_color(self, event):
        x = event.x + 1
        y = event.y + 1
        if 0 < x and x <= self.get_width() and 0 < y and y < self.get_height():
            pixel = self.get_pixel(x, y)
            print pixel
            None

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def get_image(self):
        if not self.surf:
            raise AttributeError
        elif (self.get_height() == 0 and self.get_width() == 0):
            raise ValueError
        
        return self.surf

    def get_width(self):
        if self.surf:
            return (self.surf.size)[0]
        else:
            raise AttributeError('Uninitialized picture has no width')

    def get_height(self):
        if self.surf:
            return (self.surf.size)[1]
        else:
            raise AttributeError('Uninitialized picture has no height')

    def get_pixel(self, x, y):
        return pixel.Pixel(self, x, y)

    def get_pixels(self):
        collect = []

        # we want the width and the height inclusive since Pixel() is one based
        # we increase the ranges so that we don't have to add in each iteration
        #Changed to 0-based!

        for x in range(0, self.get_width()):
            for y in range(0, self.get_height()):
                collect.append(pixel.Pixel(self, x, y))

        return collect

    def set_pixels(self, color):
        """set all the pixels in this picture to a given color"""

        try:
            image = Image.new(self.surf.mode, self.surf.size, tuple(color.get_rgb()))
            self.__initialize_picture(image, self.filename, self.title)
        except:
            raise AttributeError('set_pixels(color): Picture has not yet been initialized.')

    def write_to(self, filename):
        # if not os.path.isabs(filename):
        #    filename = media_folder + filename

        self.surf.save(filename)

    def add_rect_filled(self, acolor, x, y, w, h):
        draw = ImageDraw.Draw(self.surf)
        draw.rectangle([x, y, x + w, y + h], outline=tuple(acolor.get_rgb()),
                       fill=tuple(acolor.get_rgb()))
        del draw

    def add_rect(self, acolor, x, y, w, h, width1=1):
        draw = ImageDraw.Draw(self.surf)
        draw.rectangle([x, y, x + w, y + h], outline=tuple(acolor.get_rgb()))
        del draw

    # Draws a polygon on the image.
    def add_polygon(self, acolor, point_list):
        draw = ImageDraw.Draw(self.surf)
        draw.polygon(point_list, outline=tuple(acolor.get_rgb()))
        del draw

    def add_polygon_filled(self, acolor, point_list):
        draw = ImageDraw.Draw(self.surf)
        draw.polygon(point_list, outline=tuple(acolor.get_rgb()), fill=
                     tuple(acolor.get_rgb()))
        del draw

    def add_oval_filled(self, acolor, x, y, w, h):
        draw = ImageDraw.Draw(self.surf)
        draw.ellipse([x, y, x + w, y + h], outline=tuple(acolor.get_rgb()),
                     fill=tuple(acolor.get_rgb()))
        del draw

    def add_oval(self, acolor, x, y, w, h):
        draw = ImageDraw.Draw(self.surf)
        draw.ellipse([x, y, x + w, y + h], outline=tuple(acolor.get_rgb()))
        del draw

    def add_arc_filled(self, acolor, x, y, w, h, start, end):
        draw = ImageDraw.Draw(self.surf)
        draw.arc([x, y, x + w, y + h], start, end, outline=tuple(acolor.get_rgb()),
                 fill=tuple(acolor.get_rgb()))
        del draw

    def add_arc(self, acolor, x, y, w, h, start, end):
        draw = ImageDraw.Draw(self.surf)
        draw.arc([x, y, x + w, y + h], start, end, outline=tuple(acolor.get_rgb()))
        del draw

    def add_line(self, acolor, x1, y1, x2, y2, width1=1):
        draw = ImageDraw.Draw(self.surf)
        draw.line([x1, y1, x2, y2], fill=tuple(acolor.get_rgb()), width=
                  width1)
        del draw

    def add_text(self, acolor, x, y, string):
        global default_font
        self.add_text_with_style(acolor, x, y, string, default_font)

    def add_text_with_style(self, acolor, x, y, string, font1):
        draw = ImageDraw.Draw(self.surf)
        draw.text((x, y), text=string, fill=tuple(acolor.get_rgb()),
                  font=font1)
        del draw
        

def get_short_path(filename):
    dirs = filename.split(os.sep)
    if len(dirs) < 1:  # does split() ever get to this stage?
        return "."
    elif len(dirs) == 1:
        return dirs[0]
    else:
        return dirs[len(dirs) - 2] + os.sep + dirs[len(dirs) - 1]
