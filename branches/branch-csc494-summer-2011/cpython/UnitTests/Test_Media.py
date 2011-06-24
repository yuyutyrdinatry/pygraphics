"""
Test_Media.py
"""

import unittest
import math
import media
import color

# Constants for basic width and height.
WIDTH=10
HEIGHT=20


class MediaCreationTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_pic_default_color(self):
        """Create a WIDTH by HEIGHT picture and check for proper dimensions
        and default color."""
        pic = media.create_picture(WIDTH, HEIGHT)
        width = media.get_width(pic)
        height = media.get_height(pic)

        self.assert_(width == WIDTH,
            'expected pic width of %s, saw %s' % (WIDTH, width))

        self.assert_(height == HEIGHT,
        'expected pic width of %s, saw %s' % (HEIGHT, height))

        for p in pic:
            self.assert_(media.get_color(p) == media.white)

    def test_create_pic_color(self):
        """Create a WIDTH by HEIGHT picture and check for proper
        dimensions and color."""
        pic = media.create_picture(WIDTH, HEIGHT, media.magenta)
        width = media.get_width(pic)
        height = media.get_height(pic)

        self.assert_(width == WIDTH,
            'expected pic width of %s, saw %s' % (WIDTH, width))

        self.assert_(height == HEIGHT,
        'expected pic width of %s, saw %s' % (HEIGHT, height))

        for p in pic:
            self.assert_(media.get_color(p) == media.magenta)

    # Pixel tests.

    def test_get_pixel_top_left(self):
        """Test getting the top left pixel."""

        pic = media.create_picture(WIDTH, HEIGHT)
        p = media.get_pixel(pic, 0, 0)
        self.assert_(media.get_x(p) == 0)
        self.assert_(media.get_y(p) == 0)

    def test_get_pixel_bottom_right(self):
        """Test getting the bottom left pixel."""

        pic = media.create_picture(WIDTH, HEIGHT)
        p = media.get_pixel(pic, WIDTH - 1, HEIGHT - 1)
        self.assert_(media.get_x(p) == WIDTH - 1)
        self.assert_(media.get_y(p) == HEIGHT - 1)

    def test_pixel_set_get_RGB(self):
        """Test setting and getting the red, green, and blue of a pixel."""

        pic = media.create_picture(WIDTH, HEIGHT)
        p = media.get_pixel(pic, WIDTH - 1, HEIGHT - 1)
        media.set_red(p, 1)
        self.assert_(media.get_red(p) == 1)
        media.set_green(p, 2)
        self.assert_(media.get_green(p) == 2)
        media.set_blue(p, 3)
        self.assert_(media.get_blue(p) == 3)

    def test_pixel_set_get_color(self):
        """Test setting and getting the color of a pixel."""

        pic = media.create_picture(WIDTH, HEIGHT)
        p = media.get_pixel(pic, WIDTH - 1, HEIGHT - 1)
        c = media.aqua
        media.set_color(p, c)
        self.assert_(media.get_color(p) == media.aqua)

    # Color tests.

    def test_darken(self):
        """Test media.darken."""

        c = color.Color(100, 100, 100)
        media.darken(c)
        self.assert_(c.get_red() == 70)
        self.assert_(c.get_green() == 70)
        self.assert_(c.get_blue() == 70)

    def test_lighten(self):
        """Test media.lighten.  These depend on darken.  Boo."""

        c = color.Color(100, 100, 100)
        media.darken(c)
        media.lighten(c)
        
        new_red = c.get_red()
        new_blue = c.get_blue()
        new_green = c.get_green()
        
        self.assert_(new_red == 100,
            "Expected %s but saw %s" % (100, new_red))
        self.assert_(new_green == 100,
                "Expected %s but saw %s" % (100, new_green))
        self.assert_(new_blue == 100,
                    "Expected %s but saw %s" % (100, new_blue))

    def test_distance(self):
        """Test the distance function."""
        
        d = media.distance(media.black, media.white)
        expected = math.sqrt(pow(255, 2) * 3)
        self.assert_(d == expected, "%s %s" % (d, expected))



if __name__ == '__main__':
    unittest.main()
