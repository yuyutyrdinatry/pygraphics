from TestExecute import *
from color import *
import nose
from math import *
import media


##############################################################################
# Test functions
##############################################################################

def test_constructor_invalid():
    '''Test that Color constructor fails with invalid RGB value input.'''

    nose.tools.assert_raises(ValueError, Color, '', '', '')
    nose.tools.assert_raises(ValueError, Color, -1, -1, -1)
    nose.tools.assert_raises(ValueError, Color, 1000, 1000, 1000)


def test_constructor():
    '''Test Color constructor. Particularly, that it accepts
    normalized [0, 255] RGB values, non-normalized values (e.g. 1000),
    and str values (e.g. "1")'''

    # Test expectedly normal function calls.
    # Color bounds to [0,255] so we must check that the new and old way are
    # the same.
    input_RGB = [(0, 0, 0), (0, 0, 255), (255, 255, 255)]

    for idx in range(len(input_RGB)):
        r = input_RGB[idx][0]
        g = input_RGB[idx][1]
        b = input_RGB[idx][2]
        tester_color = Color(r, g, b)
        assert tester_color.r == r, \
            'Invalid red color component (idx=' + str(idx) + ')'
        assert tester_color.g == g, \
            'Invalid green color component (idx=' + str(idx) + ')'
        assert tester_color.b == b, \
            'Invalid blue color component (idx=' + str(idx) + ')'

        # test non-int inputs
        tester_color = Color(str(r), str(g), str(b))
        assert tester_color.r == r, \
            'Invalid red color component (idx=' + str(idx) + ')'
        assert tester_color.g == g, \
            'Invalid green color component (idx=' + str(idx) + ')'
        assert tester_color.b == b, \
            'Invalid blue color component (idx=' + str(idx) + ')'


def test_equality():
    '''Test the __eq__ method of Color.'''

    colors = [Color(0, 0, 0), Color(255, 255, 255), Color(50, 50, 50)]
    colors_equal = [Color(0, 0, 0), Color(255, 255, 255), Color(50, 50, 50)]
    colors_unequal = [Color(255, 255, 255), Color(0, 0, 0), Color(45, 45, 45)]

    for idx in range(len(colors)):
        assert colors[idx] == colors_equal[idx], \
            "Equal colors not compared properly."
        assert colors[idx] != colors_unequal[idx], \
            "Unequal colors not compared properly."


def test_distance():
    '''Test distance method for finding the euclidean distance between two
    colors.'''

    colors1 = [Color(0, 0, 0), Color(255, 255, 255), Color(0, 0, 255),
        Color(255, 255, 255)]
    colors2 = [Color(0, 0, 0), Color(255, 255, 255), Color(255, 0, 0),
        Color(0, 0, 0)]

    # Ccalculate the expected euclidean distance, i.e.
    #  sqrt(Rdist ** 2 + Gdist ** 2 + Bdist ** 2))
    expected_distance = [0, 0, sqrt(pow(255, 2) * 2), sqrt(pow(255, 2) * 3)]

    assert len(colors1) == len(colors2) == len(expected_distance), \
        'Test arrays are not mapped 1:1.'

    for idx in range(len(colors1)):
        distance1 = colors1[idx].distance(colors2[idx])
        distance2 = colors2[idx].distance(colors1[idx])
        assert distance1 == expected_distance[idx], 'Improper color distance'
        assert distance2 == distance1, \
            'Distance from color1 to color2 not equal to' \
            ' distance from color2 to color1'


def test_sub():
    '''Test Color __sub__ method.'''

    # test that color subtraction works
    colors1 = [Color(0, 0, 0), Color(255, 255, 255), Color(0, 0, 255),
        Color(255, 255, 255)]
    colors2 = [Color(0, 0, 0), Color(255, 255, 255), Color(255, 0, 0),
        Color(0, 0, 0)]

    expected_difference_one_minus_two = [Color(0, 0, 0), Color(0, 0, 0),
        Color(0, 0, 255), Color(255, 255, 255)]
    expected_difference_two_minus_one = [Color(0, 0, 0), Color(0, 0, 0),
        Color(255, 0, 0), Color(0, 0, 0)]

    assert len(colors1) == len(colors2) == \
        len(expected_difference_one_minus_two) == \
        len(expected_difference_two_minus_one), \
        'Test arrays are not mapped 1:1'

    for idx in range(len(colors1)):
        # ensure that both difference and subtract work the same
        sub1 = colors1[idx] - colors2[idx]
        sub2 = colors2[idx] - colors1[idx]
        assert sub1 == expected_difference_one_minus_two[idx], \
            'Unexpected difference returned (one-two)'
        assert sub2 == expected_difference_two_minus_one[idx], \
            'Unexpected difference returned (two-one)'


def test_add():
    '''Test Color __add__ method.'''

    # test that color subtraction works
    colors1 = [Color(1, 1, 1), Color(0, 64, 255), Color(255, 255, 255),
        Color(34, 78, 12)]
    colors2 = [Color(1, 1, 1), Color(0, 64, 255), Color(255, 255, 255),
        Color(34, 78, 12)]
    expected_sum = [Color(2, 2, 2), Color(0, 128, 255), Color(255, 255, 255),
        Color(68, 156, 24)]

    assert len(colors1) == len(colors2) == len(expected_sum), \
        'Test arrays are not mapped 1:1'

    for idx in range(len(colors1)):
        # Ensure that both difference and subtract work the same.
        sum = colors1[idx] + colors2[idx]
        assert sum == expected_sum[idx], 'Unexpected sum returned.'


def test_set_get_invalid_RGB():
    '''Test setting and getting invalid RGB values from Color object.'''

    c = Color(0, 0, 0)
    try:
        c.set_red(-1)
        assert False, "set_red(-1) did not raise a ValueError."
    except ValueError:
        pass

    try:
        c.set_green(-1)
        assert False, "set_green(-1) did not raise a ValueError."
    except ValueError:
        pass
        
    try:
        c.set_blue(-1)
        assert False, "set_blue(-1) did not raise a ValueError."
    except ValueError:
        pass

    try:
        c.set_red(256)
        assert False, "set_red(256) did not raise a ValueError."
    except ValueError:
        pass

    try:
        c.set_green(256)
        assert False, "set_green(256) did not raise a ValueError."
    except ValueError:
        pass

    try:
        c.set_blue(256)
        assert False, "set_blue(256) did not raise a ValueError."
    except ValueError:
        pass


def test_set_get_RGB():
    '''Test setting and getting RGB values from Color object.'''

    # test the setters/getters of RGB components
    color_arrays = [[1, 1, 1], [0, 64, 255], [255, 255, 255], [34, 78, 12]]
    tester_color = Color(0, 0, 0)

    for color_array in color_arrays:

        # set individually
        tester_color.set_red(color_array[0])
        tester_color.set_green(color_array[1])
        tester_color.set_blue(color_array[2])

        assert tester_color.get_rgb() == tuple(color_array)
        assert tester_color.get_red() == color_array[0], \
            'Different red component returned'
        assert tester_color.get_green() == color_array[1], \
            'Different green component returned'
        assert tester_color.get_blue() == color_array[2], \
            'Different blue component returned'


def test_eq():
    '''Test __eq__ and __ne__ methods from Color object.'''

    # test the setters/getters of RGB components
    colors = [Color(1, 1, 1), Color(0, 64, 255), Color(255, 255, 255),
        Color(34, 78, 12)]
    colors_eq = [Color(1, 1, 1), Color(0, 64, 255), Color(255, 255, 255),
        Color(34, 78, 12)]
    colors_not_eq = [Color(0, 0, 0), Color(1, 1, 1), Color(2, 2, 2),
        Color(3, 78, 12)]

    for idx in range(len(colors)):
        assert colors[idx] == colors_eq[idx]
        assert colors[idx] != colors_not_eq[idx]


def test_copy():
    '''Test copy method from Color object.'''

    # test the setters/getters of RGB components
    colors = [Color(1, 1, 1), Color(0, 64, 255), Color(255, 255, 255),
        Color(34, 78, 12)]

    for idx in range(len(colors)):
        color_copy = colors[idx].copy()
        color_copy.set_red(0)
        color_copy.set_green(0)
        color_copy.set_blue(0)
        assert colors[idx] != color_copy


def test_make_lighter_darker():
    '''Test make_lighter and make_darker methods of Color object.'''

    # Not quite sure how to test this other than comparing the resulting
    # color's values.
    # TODO: revisit this when we allow arbitrary changes in intensity.
    color_arrays = [[1, 1, 1], [0, 64, 255], [255, 255, 255], [34, 78, 12]]

    for color_array in color_arrays:
        lighter = Color(color_array[0], color_array[1], color_array[2])
        darker = Color(color_array[0], color_array[1], color_array[2])

        lighter.make_lighter()
        darker.make_darker()

        # we expect the lighter color to have values closer to white
        assert lighter.get_red() >= color_array[0], \
            'Red component is not lighter'
        assert lighter.get_green() >= color_array[1], \
            'Green component is not lighter'
        assert lighter.get_blue() >= color_array[2], \
            'Blue component is not lighter'

        # we expect the darker color to have values closer to black
        assert darker.get_red() <= color_array[0], \
            'Red component is not darker'
        assert darker.get_green() <= color_array[1], \
            'Green component is not darker'
        assert darker.get_blue() <= color_array[2], \
            'Blue component is not darker'


def test_to_string():
    '''Test __str__ and __repr__ methods of Color object.'''

    color_arrays = [[1, 1, 1], [0, 64, 255], [255, 255, 255], [34, 78, 12]]
    for color_array in color_arrays:

        # compare strings
        expected_str = 'Color r=' + str(color_array[0]) + \
            ' g=' + str(color_array[1]) + \
            ' b=' + str(color_array[2])

        expected_repr = 'Color(' + str(color_array[0]) + ', ' + \
            str(color_array[1]) + ', ' + str(color_array[2]) + ')'

        new_color = Color(color_array[0], color_array[1], color_array[2])

        assert str(new_color) == expected_str, \
            'Color strings do not match:\n' + str(new_color) + \
            '\n' + expected_str
        assert repr(new_color) == expected_repr, \
            'Color strings do not match:\n' + str(new_color) + \
                '\n' + expected_repr


def test_make_new_color():
    '''Test picture module functions create_color to ensure it creates
    Color objects identical to ones created manually.'''

    color_arrays = [[1, 1, 1], [0, 64, 255], [255, 255, 255], [34, 78, 12]]
    for color_array in color_arrays:
        # create using all three ways
        color_make = media.create_color(color_array[0], color_array[1],
            color_array[2])
        color_manual = Color(color_array[0], color_array[1],
            color_array[2])
        assert color_make == color_manual, \
            'Colors not the same (' + str(color_manual) + ')'


def test_non_color_object_call():
    '''Test to ensure that all the picture global convenience functions fail
    on non-Picture objects.'''

    nose.tools.assert_raises(AttributeError, media.distance, DummyClass(),
        DummyClass())
    nose.tools.assert_raises(AttributeError, media.distance, Color(0, 0, 0),
        DummyClass())
    nose.tools.assert_raises(AttributeError, media.distance, DummyClass(),
        Color(0, 0, 0))
    nose.tools.assert_raises(AttributeError, media.darken, DummyClass())
    nose.tools.assert_raises(AttributeError, media.lighten, DummyClass())


if __name__ == '__main__':
    nose.runmodule()
