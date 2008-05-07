#import unittest
#import os.path
from TestExecute import *
from picture import *
import nose
#from media import *

###############################################################################
# Setup function
##############################################################################
def setup_function():
	'''A setup function to be called by nose at the beginning of every test.
	Creates global variables used in most tests.'''
	global black_array, white_array, black_tuple, white_tuple, img, large_img
	black_array, white_array = [0,0,0], [255,255,255]
	black_tuple, white_tuple = tuple(black_array), tuple(white_array)
	# set up a small picture
	img = Picture()	
	img.surf = Image.new("RGB",(2,2))
	img.surf.putdata([black_tuple,white_tuple,white_tuple,black_tuple])
	img.pixels = img.surf.load()
	# set up the larger picture
	large_img = Picture()
	large_img.surf = Image.new("RGB",(4,4))
	large_img.surf.putdata([black_tuple,white_tuple,black_tuple,white_tuple,\
							 white_tuple,black_tuple,white_tuple,black_tuple,\
							 black_tuple,white_tuple,black_tuple,white_tuple,\
							 white_tuple,black_tuple,white_tuple,black_tuple,])
	large_img.pixels = large_img.surf.load()

def teardown_function():
	'''A teardown function to be called by nose at the end of every test.
	Destroys global variables created in setup.'''
	global black_array, white_array, black_tuple, white_tuple, img, large_img
	del black_array, white_array, black_tuple, white_tuple, img, large_img

###############################################################################
# Test functions
##############################################################################

@nose.with_setup(setup_function, teardown_function)
def test_constructor_invalid():
	'''Test the constructor of Pixel on improper input, Errors expected.'''
	# NOTE: pixels is of type [x=[y=[RGB]]], and x,y are ONE based
	nose.tools.assert_raises(ValueError, Pixel, None, 0, 0)
	nose.tools.assert_raises(IndexError, Pixel, img, 2, 2)
	nose.tools.assert_raises(IndexError, Pixel, img, -10, 10)
	
@nose.with_setup(setup_function, teardown_function)
def test_constructor():
	'''Test the constructor of Pixel on proper input.'''
	try:
		#positive pixel coordinates
		for x in range(img.surf.size[0]):
			for y in range(img.surf.size[1]):
				tester_pixel = Pixel(img, x, y) # x=0, y=0
				assert tester_pixel.x == x, 'Invalid x coordinate initialized'
				assert tester_pixel.y == y, 'Invalid y coordinate initialized'
				if x == y:
					assert list(tester_pixel.pix.pixels[tester_pixel.x,tester_pixel.y]) == black_array, 'Invalid pixel color initialized'
				else:
					assert list(tester_pixel.pix.pixels[tester_pixel.x,tester_pixel.y]) == white_array, 'Invalid pixel color initialized'
	except Exception, e:
		assert False, "Failed on proper construction input: " + str(e)

@nose.with_setup(setup_function, teardown_function)
def test_constructor_wraparound():
	'''Test the constructor of Pixel on proper input. Use wraparound coordinates.'''
	try:
		for x in range(0, -img.surf.size[0], -1):
			for y in range(0, img.surf.size[1], -1):
				tester_pixel = Pixel(img, x, y) # x=0, y=0
				assert tester_pixel.x == abs(x), 'Invalid x coordinate initialized'
				assert tester_pixel.y == abs(y), 'Invalid y coordinate initialized'
				if x == y:
					assert list(tester_pixel.pix.pixels[tester_pixel.x,tester_pixel.y]) == black_array, 'Invalid pixel color initialized'
				else:
					assert list(tester_pixel.pix.pixels[tester_pixel.x,tester_pixel.y]) == white_array, 'Invalid pixel color initialized'
	except Exception, e:
		assert False, "Failed on proper construction input: " + str(e)

@nose.with_setup(setup_function, teardown_function)
def test_has_color():
	'''Test the has_color and has_color_values methods of Pixel.'''
	tester_pixel = Pixel(img, 0, 0)
	tester_color_arrays = [(0, 0, 0), (255, 255, 255), (128, 128, 128)]
	for color_array in tester_color_arrays:
		tester_pixel.pix.pixels[tester_pixel.x, tester_pixel.y] = color_array
		tester_color = Color(0,0,0)
		tester_color.set_rgb(color_array)
		assert tester_pixel.has_color(tester_color), "has_color failed on proper Color input"
		assert tester_pixel.has_color_values(color_array), "has_color_value failed on proper value input"

@nose.with_setup(setup_function, teardown_function)
def test_set_RGB_inbounds():
	'''Test setting RGB values for Pixel.'''
	# TODO: also test for Alpha if we add support for that
	tester_pixel = Pixel(img, 0, 0)
	assert tester_pixel.has_color_values(black_array), 'Improper color component, should be [0, 0, 0]'
	tester_pixel.set_red(0) # empty set
	tester_pixel.set_green(0)
	tester_pixel.set_blue(0)
	assert tester_pixel.has_color_values(black_array), 'Improper color component, should be [0, 0, 0]'
	tester_pixel.set_red(255) # set new red
	assert tester_pixel.has_color_values([255, 0, 0]), 'Improper color component, should be [255, 0, 0]'
	tester_pixel.set_blue(128) # set new blue
	assert tester_pixel.has_color_values([255, 0, 128]), 'Improper color component, should be [255, 0, 128]'
	tester_pixel.set_green(64) # set green
	assert tester_pixel.has_color_values([255, 64, 128]), 'Improper color component, should be [255, 64, 128]'
	tester_pixel.set_blue(255); tester_pixel.set_green(255)
	assert tester_pixel.has_color_values(white_array), 'Improper color component, should be [255, 255, 255]'

@nose.with_setup(setup_function, teardown_function)
def test_set_RGB_outbounds():
	'''Test setting RGB values that are out of bounds for Pixel.'''
	outbounds = [-1, -10, 256, 300]
	tester_pixel = Pixel(img, 0, 0)
	for value in outbounds:
		nose.tools.assert_raises(ValueError, tester_pixel.set_red, value)
		nose.tools.assert_raises(ValueError, tester_pixel.set_green, value)
		nose.tools.assert_raises(ValueError, tester_pixel.set_blue, value)


@nose.with_setup(setup_function, teardown_function)
def test_get_RGB():
	'''Test getting Pixel RGB values methods.'''
	tester_pixel = Pixel(img, 0, 0)
	assert tester_pixel.has_color_values(black_array), 'Improper color gotten'
	assert tester_pixel.get_red() == 0, 'Improper color gotten'
	assert tester_pixel.get_green() == 0, 'Improper color gotten'
	assert tester_pixel.get_blue() == 0, 'Improper color gotten'
	
	# set different color values
	tester_pixel.set_red(64)
	tester_pixel.set_green(128)
	tester_pixel.set_blue(32)
	assert tester_pixel.get_red() == 64, 'Improper color gotten'
	assert tester_pixel.get_green() == 128, 'Improper color gotten'
	assert tester_pixel.get_blue() == 32, 'Improper color gotten'

@nose.with_setup(setup_function, teardown_function)
def test_set_get_color():
	'''Test the setting and getting Color for Pixel.'''
	colors = [Color(0, 0, 0), Color(-1, -1, -1), Color(0, 64, 32), Color(255, 255, 255)]
	tester_pixel = Pixel(img, 0, 0)
	for color in colors:
		# ensure that the colors are the same after setting and getting
		tester_pixel.set_color(color)
		assert tester_pixel.has_color(color), 'Colors do not match (' + str(tester_pixel) + ', ' + str(color) + ')'
		assert tester_pixel.get_color() == color, 'Colors do not match (' + str(tester_pixel.get_color()) + ', ' + str(color) + ')'

@nose.with_setup(setup_function, teardown_function)
def test_has_XY():
	'''Test the has_XY method of Pixel.'''
	len_x = large_img.surf.size[0]
	len_y = large_img.surf.size[1]
	
	# test in range x, y
	for x in range(len_x):
		for y in range(len_y):
			tester_pixel = Pixel(large_img, x, y)
			assert tester_pixel.has_XY(x, y), "has_XY failed on proper in-bound input"
			
	# test out of range x, y (IndexError expected)
	for x in range(len_x, len_x * 2):
		for y in range(len_y, len_y * 2):
			tester_pixel = Pixel(large_img, x % len_x, y % len_y)
			nose.tools.assert_raises(IndexError, tester_pixel.has_XY, x, y)

@nose.with_setup(setup_function, teardown_function)
def test_get_XY():
	'''Test that get_x and get_y return valid indices within ranges x=[0, width], y=[0, height]'''
	width = large_img.get_width()
	height = large_img.get_height()
	
	input_coordinates = [(0, 0), (3, 3), (-1, -1), (-2, -2), (-3, -3)]
	expected_coordinates = [(0, 0), (3, 3), (3, 3), (2, 2), (1, 1)]	# wrap around values will be bounded
	assert len(input_coordinates) == len(expected_coordinates), 'Test arrays are not mapped 1:1'
	# test each of the input coordinates, making sure they map to the correct expected coords
	for idx in range(len(input_coordinates)):
		tester_pixel = Pixel(large_img, input_coordinates[idx][0], input_coordinates[idx][1])
		assert tester_pixel.has_XY(expected_coordinates[idx][0], expected_coordinates[idx][1]), 'Improper XY coordinates (' + str(tester_pixel.get_x()) + ', ' + str(tester_pixel.get_y()) + ')'	

@nose.with_setup(setup_function, teardown_function)
def test_non_pixel_object_call():
	'''Test that picture global convenience functions called on non-Pixel class raise appropriate ValueError.'''
	nose.tools.assert_raises(ValueError, set_red, DummyClass(), 0)
	nose.tools.assert_raises(ValueError, set_green, DummyClass(), 0)
	nose.tools.assert_raises(ValueError, set_blue, DummyClass(), 0)
	nose.tools.assert_raises(ValueError, get_red, DummyClass())
	nose.tools.assert_raises(ValueError, get_green, DummyClass())
	nose.tools.assert_raises(ValueError, get_blue, DummyClass())
	nose.tools.assert_raises(ValueError, get_color, DummyClass())
	nose.tools.assert_raises(ValueError, set_color, DummyClass(), None)
	nose.tools.assert_raises(ValueError, set_color, Pixel(img, 1, 1), None)
	nose.tools.assert_raises(ValueError, get_x, DummyClass())
	nose.tools.assert_raises(ValueError, get_y, DummyClass())
	
if __name__ == '__main__':
	nose.runmodule()
	
		