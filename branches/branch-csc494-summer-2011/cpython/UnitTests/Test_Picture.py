from TestExecute import *
from picture import *
import nose
import media

IMAGE_TYPES = ['bmp', 'gif', 'jpg']
BLESSED_SAVE_LOC_PREFIX = resi('saved.')
SAVE_LOC_PREFIX = resi('saved.tmp.')


###############################################################################
# Setup/Teardown Functions
##############################################################################

def setup_function():
    """A setup function to be called by nose at the beginning of every test.
    Creates global variables used in most tests."""
    global pict
    pict = Picture(1, 1)


def teardown_function():
    """A teardown function to be called by nose at the end of every test.
    Destroys global variables created in setup."""
    global pict
    del pict


###############################################################################
# Helper functions
##############################################################################

def ensure_files_equal(filename1, filename2):
    """Raise ValueError if two image files referred to by (filename1,
    filename2) are not identical."""

    p1 = Picture(filename=filename1)
    p2 = Picture(filename=filename2)
    ensure_pictures_equal(p1, p2)


def ensure_pictures_equal(p1, p2):
    """Raise ValueError if Pictures p1 and p1 are not equal in terms of
    dimensions and color."""

    image1 = p1.get_image()
    image2 = p2.get_image()
    ensure_images_equal(image1, image2)


def ensure_images_equal(image1, image2):
    """Raise ValueError if Pictures p1 and p1 are not equal in terms of
    dimensions and color."""

    pixels1 = image1.load()
    pixels2 = image2.load()
    if not image1.size == image2.size:
        raise ValueError('Improper dimensions)')
    for x in range(image1.size[0]):
        for y in range(image1.size[1]):
            px1 = pixels1[x, y]
            px2 = pixels2[x, y]
            if not px1 == px2:
                raise ValueError('Pictures not equal')


def ensure_picture_has_color(picture, color):
    """Raise ValueError if Picture picture has all pixels with Color color."""

    pixels = picture.get_pixels()
    for pixel in pixels:
        if not ((pixel.get_red() == color.get_red())
            and (pixel.get_green() == color.get_green())
            and (pixel.get_blue() == color.get_blue())):
            raise ValueError('Picture does not have solid color')


###############################################################################
# Test functions
##############################################################################

def test_invalid_input_constructor():
    """Test the Picture class constructor with invalid input"""

    nose.tools.assert_raises(IOError, Picture, filename='nosuchfile')
    nose.tools.assert_raises(TypeError, Picture)
    nose.tools.assert_raises(ValueError, Picture, image='thisisnotanimage')
    nose.tools.assert_raises(ValueError, Picture, 0, 0)
    nose.tools.assert_raises(ValueError, Picture, 0, 1)
    nose.tools.assert_raises(ValueError, Picture, -1, -1)


@nose.with_setup(setup_function, teardown_function)
def test_wh_constructor():
    """Test the Picture class constructor with width and height"""

    tester_pict = Picture(10, 10)
    if tester_pict.get_image():
        img = tester_pict.get_image()
        assert img.size[0] == 10, 'New Picture has incorrect width'
        assert img.size[1] == 10, 'New Picture has incorrect height'
        assert tester_pict.filename == '', 'New Picture has incorrect filename'
        assert tester_pict.title == '', 'New Picture has incorrect filename'
    else:
        assert False, 'New Picture has no display image'


@nose.with_setup(setup_function, teardown_function)
def test_image_constructor():
    """Test the Picture class constructor with an image"""

    tester_image = Image.new("RGB", (10, 10))
    tester_pict = Picture(image=tester_image)
    if tester_pict.get_image():
        img = tester_pict.get_image()
        assert img.size[0] == 10, 'New Picture has incorrect width'
        assert img.size[1] == 10, 'New Picture has incorrect height'
        assert tester_pict.filename == '', 'New Picture has incorrect filename'
        assert tester_pict.title == '', 'New Picture has incorrect filename'
    else:
        assert False, 'New Picture has no display image'


@nose.with_setup(setup_function, teardown_function)
def test_filename_constructor():
    """Test the Picture class constructor with a filename"""

    filepath = resi("white.bmp")
    tester_pict = Picture(filename=filepath)
    if tester_pict.get_image():
        img = tester_pict.get_image()
        pixels = img.load()
        assert tester_pict.image.size == (50, 50), "Invalid Picture dimensions"
        assert len(pixels[0, 0]) == 3, "Invalid Picture depth."
        assert tester_pict.filename == filepath, \
            "Improper filename (%s) for loaded image" % pict.filename
        assert tester_pict.title == 'images/white.bmp', \
            "Improper title (%s) for loaded image" % pict.title
    else:
        assert False, 'New Picture has no display image'


@nose.with_setup(setup_function, teardown_function)
def test_get_width_height():
    """Test get_height and get_width with a valid Picture"""

    # create image
    dimensions = [(1, 1), (50, 50), (1, 5), (10, 1)]
    for idx in range(len(dimensions)):
        w = dimensions[idx][0]
        h = dimensions[idx][1]
        tester_pict = Picture(w, h)
        assert tester_pict.get_width() == w, 'Invalid image width'
        assert tester_pict.get_height() == h, 'Invalid image height'
        del tester_pict


@nose.with_setup(setup_function, teardown_function)
def test_has_coordinates():
    """Test has_coordinates with a valid Picture"""

    assert pict.has_coordinates(0, 0)
    assert not pict.has_coordinates(0, 1)
    assert not pict.has_coordinates(1, 1)
    assert not pict.has_coordinates(1, 0)


@nose.with_setup(setup_function, teardown_function)
def test_to_string():
    """Test str() functionality with a valid Picture"""
    filename_prefix = 'white.'
    failed = False
    error_res = ''
    # for each of the supported file types
    for suffix in IMAGE_TYPES:
        filename = filename_prefix + suffix
        file = resi(filename)
        # try and load the test file of that type
        try:
            tester_pict = Picture(filename=file)
            h = tester_pict.get_height()
            w = tester_pict.get_width()
            assert str(tester_pict) == \
                "Picture, filename=%s height=%d width=%d" % (file, h, w), \
            "Invalid str conversion, str was " + str(tester_pict)
        except ValueError, e:
            error_res += 'Error loading images of type: ' + suffix + \
                " (" + str(e) + ")"
            failed = True
    # there was at least one error loading the test files
    if failed:
        assert False, error_res


@nose.with_setup(setup_function, teardown_function)
def test_title_created_image():
    """Test title functionality of Picture with a created image."""

    assert pict.get_title() == '', "Improper title " + pict.get_title()
    pict.set_title('asdf')
    assert pict.get_title() == 'asdf', "Improper title " + pict.get_title()


@nose.with_setup(setup_function, teardown_function)
def test_title_and_filename():
    """Test title functionality of Picture with a loaded image."""

    filepath = resi('white.bmp')
    tester_pict = Picture(filename=filepath)
    assert tester_pict.get_title() == 'images/white.bmp', \
        "Improper title " + pict.get_title()
    assert tester_pict.get_filename() == filepath, \
        "Improper filename " + pict.get_filename()
    tester_pict.set_title('asdf')
    assert tester_pict.get_title() == 'asdf', \
        "Improper title " + pict.get_title()


@nose.with_setup(setup_function, teardown_function)
def test_set_get_image():
    """Test get_image and set_image with a valid Picture."""

    # ensure that the Image has the same properties as the Picture
    # test created blank image and loaded image
    # create/load picture
    r = 255
    g = 255
    b = 255
    tester_images = [Image.new("RGB", (10, 10), (r, g, b)),
                     Image.new("RGB", (50, 50), (r, g, b))]
    sizes = [(10, 10), (50, 50)]
    # convert to PIL image and ensure properties are the same
    i = 0
    for tester_image in tester_images:
        pict.set_image(tester_image)
        assert pict.image.mode == 'RGB', "Improper image color bands"
        assert pict.image.size == sizes[i], "Improper image size"
        image = pict.get_image()
        assert image.mode == 'RGB', "Improper image color bands"
        assert image.size == sizes[i], "Improper image size"
        # ensure all the pixels are of the correct color
        correct_color = True
        image_pixels = list(image.getdata())
        for pixel in image_pixels:
            if not pixel == (r, g, b):
                correct_color = False
        if not correct_color:
            assert False, 'Invalid image colors (' + str(i) + ')'
        i += 1


@nose.with_setup(setup_function, teardown_function)
def test_copy():
    """Test copy on a valid Picture."""

    pict2 = pict.copy()
    p1 = pict.get_pixel(0, 0)
    p2 = pict2.get_pixel(0, 0)
    p2.set_red(0)
    assert p1.get_color() != p2.get_color(), "Not a true deep copy"


@nose.with_setup(setup_function, teardown_function)
def test_crop():
    """Test crop on a valid Picture."""

    copy = pict.copy()
    p1 = pict.get_pixel(0, 0)
    p2 = copy.get_pixel(0, 0)
    p2.set_red(0)
    assert p1.get_color() != p2.get_color(), "Not a true deep copy"


@nose.with_setup(setup_function, teardown_function)
def test_get_pixel():
    """Test get_pixel on a valid Picture."""

    # NOTE: indices are ONE based. Indices are now ZERO based.
    # out of bounds indices
    # IMAGE SIZE: 0
    try:
        pict.get_pixel(0, 0)
    except Exception, e:
        assert False, \
            "Exception: " + str(e) + " thrown when getting valid pixel"

    nose.tools.assert_raises(IndexError, pict.get_pixel, 1, 0)
    nose.tools.assert_raises(IndexError, pict.get_pixel, -1, -1)
    nose.tools.assert_raises(IndexError, pict.get_pixel, 2, 2)
    nose.tools.assert_raises(IndexError, pict.get_pixel, 50, 50)


@nose.with_setup(setup_function, teardown_function)
def test_get_pixels():
    """Test get_pixels on a valid Picture."""

    dimensions = [(1, 1), (10, 1), (1, 10), (10, 10)]
    expected_len = [1, 10, 10, 100]
    assert len(dimensions) == len(expected_len), 'Test arrays are mapped 1:1'

    for idx in range(len(dimensions)):
        tester_pict = Picture(dimensions[idx][0], dimensions[idx][1])
        assert len([pixel for pixel in tester_pict]) == expected_len[idx], \
            'Invalid number of pixels returned (' + str(idx) + ')'
        del tester_pict


@nose.with_setup(setup_function, teardown_function)
def test_write_to_large_image():
    """Test writing a large valid Picture to a file"""

    # invalid file types
    tester_pict = Picture(filename=BLESSED_SAVE_LOC_PREFIX + 'bmp')
    nose.tools.assert_raises(ValueError, tester_pict.save_as,
        SAVE_LOC_PREFIX + 'tmp')

    # ensure all of our types hold
    for suffix in IMAGE_TYPES:
        try:
            tester_pict.save_as(SAVE_LOC_PREFIX + suffix)
            # compare with saved copies
            ensure_files_equal(BLESSED_SAVE_LOC_PREFIX + suffix,
                SAVE_LOC_PREFIX + suffix)
        except KeyError:
            assert False, \
                'Failed saving created image to (' + suffix + ') files'


@nose.with_setup(setup_function, teardown_function)
def test_write_to_loaded_image():
    """Test writing a loaded Picture to a file."""
    tester_save_loc_prefix = resi('white.tmp.')
    blessed_tester_save_loc_prefix = resi('white.')
    for suffix in IMAGE_TYPES:
        tester_pict = Picture(filename=blessed_tester_save_loc_prefix + suffix)
        try:
            tester_pict.save_as(tester_save_loc_prefix + suffix)

            # compare with saved copies
            ensure_files_equal(blessed_tester_save_loc_prefix + suffix,
                tester_save_loc_prefix + suffix)

        except KeyError:
            assert False, \
                'Failed saving loaded image to (' + suffix + ') files'
        del tester_pict


def test_get_picture_with_height():
    # TODO
    print "TBD"


def test_load_and_show_picture():
    # TODO
    print "TBD"


def test_get_transform_enclosing_rect():
    # TODO
    print "TBD"


@nose.with_setup(setup_function, teardown_function)
def test_make_picture():
    """Test making picture from a valid file."""
    # ensure that this returns an identical picture from one created manually
    image_loc = resi('white.bmp')
    tester_pict = media.load_picture(image_loc)
    manual_tester_pict = Picture(filename=image_loc)
    ensure_pictures_equal(tester_pict, manual_tester_pict)


@nose.with_setup(setup_function, teardown_function)
def test_non_picture_object_call():
    """Test that all the picture global convenience functions fail on
    non-Picture objects."""
    nose.tools.assert_raises(AttributeError, media.get_pixel, DummyClass(),
        0, 0)
    nose.tools.assert_raises(TypeError, media.get_pixels, DummyClass())
    nose.tools.assert_raises(AttributeError, media.get_width, DummyClass())
    nose.tools.assert_raises(AttributeError, media.get_height, DummyClass())
    nose.tools.assert_raises(AttributeError, media.show, DummyClass())
    nose.tools.assert_raises(AttributeError, media.add_line, DummyClass(),
        0, 0, 0, 0, None)
    nose.tools.assert_raises(AttributeError, media.add_text, DummyClass(),
        0, 0, '', None)
    nose.tools.assert_raises(AttributeError, media.add_rect, DummyClass(),
        0, 0, 0, 0, None)
    nose.tools.assert_raises(AttributeError, media.add_rect_filled,
        DummyClass(), 0, 0, 0, 0, None)
    nose.tools.assert_raises(AttributeError, media.save_as, DummyClass(),
        'asdf')


@nose.with_setup(setup_function, teardown_function)
def test_get_short_path():
    """Test that the short path is returned correctly by function
    get_short_path."""
    assert get_short_path('') == '', 'Invalid short path'
    assert get_short_path('a.img') == 'a.img', 'Invalid short path'
    assert get_short_path(
        os.path.join('b', 'a.img')) == os.path.join('b', 'a.img'), \
        'Invalid short path'
    assert get_short_path(
        os.path.join(
            'c', os.path.join('b', 'a.img'))) == os.path.join('b', 'a.img'), \
            'Invalid short path'

if __name__ == '__main__':
    nose.runmodule()
