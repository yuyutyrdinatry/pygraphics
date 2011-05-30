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
	global black_array, white_array, black_tuple, white_tuple, pict, large_pict
	black_array, white_array = [0,0,0], [255,255,255]
	black_tuple, white_tuple = tuple(black_array), tuple(white_array)
	# set up a small picture
	pict = Picture(image=Image.new("RGB",(2,2)))	
	pict.image.putdata([black_tuple,white_tuple,white_tuple,black_tuple])
	pict.pixels = pict.image.load()
	# set up the larger picture
	large_pict = Picture(image=Image.new("RGB",(4,4)))	
	large_pict.image.putdata([black_tuple,white_tuple,black_tuple,white_tuple,\
							 white_tuple,black_tuple,white_tuple,black_tuple,\
							 black_tuple,white_tuple,black_tuple,white_tuple,\
							 white_tuple,black_tuple,white_tuple,black_tuple,])
	large_pict.pixels = large_pict.image.load()

def teardown_function():
	'''A teardown function to be called by nose at the end of every test.
	Destroys global variables created in setup.'''
	
	global black_array, white_array, black_tuple, white_tuple, pict, large_pict
	del black_array, white_array, black_tuple, white_tuple, pict, large_pict

def pixel_has_color(pixel, color):
    '''Return True if Pixel pixel has Color color.'''
        
    return (pixel.get_red() == color.get_red() and
            pixel.get_green() == color.get_green() and
            pixel.get_blue() == color.get_blue())

def pixel_has_color_values(pixel, color_list):
    '''Return True if Pixel pixel has RGB values of list color_list.
    
    Note: color_list is expected to be in the following format, [R, G, B], 
    where RGB are int values.'''
        
    return (pixel.get_red() == color_list[0] and
            pixel.get_green() == color_list[1] and
            pixel.get_blue() == color_list[2])

def pixel_has_XY(pixel, x, y):
    '''Return True if Pixel pixel has coordinates int x and int y.'''
    
    return pixel.get_x() == x and pixel.get_y() == y


###############################################################################
# Test functions
##############################################################################

@nose.with_setup(setup_function, teardown_function)
def test_constructor():
	'''Test the constructor of Pixel on proper input.'''
	try:
		#positive pixel coordinates
		for x in range(pict.image.size[0]):
			for y in range(pict.image.size[1]):
				tester_pixel = pixel.Pixel(pict.pixels, x, y) # x=0, y=0
				assert tester_pixel.x == x, 'Invalid x coordinate initialized'
				assert tester_pixel.y == y, 'Invalid y coordinate initialized'
				if x == y:
					assert list(tester_pixel.pixels[tester_pixel.x,tester_pixel.y]) == black_array, 'Invalid pixel color initialized'
				else:
					assert list(tester_pixel.pixels[tester_pixel.x,tester_pixel.y]) == white_array, 'Invalid pixel color initialized'
	except Exception, e:
		assert False, "Failed on proper construction input: " + str(e)

@nose.with_setup(setup_function, teardown_function)
def test_set_RGB_inbounds():
	'''Test setting RGB values for Pixel.'''
	# TODO: also test for Alpha if we add support for that
	tester_pixel = pixel.Pixel(pict.pixels, 0, 0)
	assert pixel_has_color_values(tester_pixel, black_array), 'Improper color component, should be [0, 0, 0]'
	tester_pixel.set_red(0) # empty set
	tester_pixel.set_green(0)
	tester_pixel.set_blue(0)
	assert pixel_has_color_values(tester_pixel, black_array), 'Improper color component, should be [0, 0, 0]'
	tester_pixel.set_red(255) # set new red
	assert pixel_has_color_values(tester_pixel, [255, 0, 0]), 'Improper color component, should be [255, 0, 0]'
	tester_pixel.set_blue(128) # set new blue
	assert pixel_has_color_values(tester_pixel, [255, 0, 128]), 'Improper color component, should be [255, 0, 128]'
	tester_pixel.set_green(64) # set green
	assert pixel_has_color_values(tester_pixel, [255, 64, 128]), 'Improper color component, should be [255, 64, 128]'
	tester_pixel.set_blue(255)
	tester_pixel.set_green(255)
	assert pixel_has_color_values(tester_pixel, white_array), 'Improper color component, should be [255, 255, 255]'

@nose.with_setup(setup_function, teardown_function)
def test_set_RGB_outbounds():
	'''Test setting RGB values that are out of bounds for Pixel.'''
	outbounds = [-1, -10, 256, 300]
	tester_pixel = pixel.Pixel(pict.pixels, 0, 0)
	for value in outbounds:
		nose.tools.assert_raises(ValueError, tester_pixel.set_red, value)
		nose.tools.assert_raises(ValueError, tester_pixel.set_green, value)
		nose.tools.assert_raises(ValueError, tester_pixel.set_blue, value)


@nose.with_setup(setup_function, teardown_function)
def test_get_RGB():
	'''Test getting Pixel RGB values methods.'''
	tester_pixel = pixel.Pixel(pict.pixels, 0, 0)
	assert pixel_has_color_values(tester_pixel, black_array), 'Improper color gotten'
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
	colors = [color.Color(0, 0, 0), color.Color(0, 64, 32), color.Color(255, 255, 255)]
	tester_pixel = pixel.Pixel(pict.pixels, 0, 0)
	for col in colors:
		# ensure that the colors are the same after setting and getting
		tester_pixel.set_color(col)
		assert pixel_has_color(tester_pixel, col), 'Colors do not match (' + str(tester_pixel) + ', ' + str(col) + ')'
		assert tester_pixel.get_color() == col, 'Colors do not match (' + str(tester_pixel.get_color()) + ', ' + str(col) + ')'
			
@nose.with_setup(setup_function, teardown_function)
def test_get_XY():
	'''Test that get_x and get_y return valid indices within ranges x=[0, width], y=[0, height]'''
	width = large_pict.get_width()
	height = large_pict.get_height()
	
	input_coordinates = [(0, 0), (3, 3), (2, 2), (1, 1)]
	expected_coordinates = [(0, 0), (3, 3), (2, 2), (1, 1)]	# wrap around values will be bounded
	assert len(input_coordinates) == len(expected_coordinates), 'Test arrays are not mapped 1:1'
	# test each of the input coordinates, making sure they map to the correct expected coords
	for idx in range(len(input_coordinates)):
		tester_pixel = pixel.Pixel(large_pict.pixels, input_coordinates[idx][0], input_coordinates[idx][1])
		assert pixel_has_XY(tester_pixel, expected_coordinates[idx][0], expected_coordinates[idx][1]), 'Improper XY coordinates (' + str(tester_pixel.get_x()) + ', ' + str(tester_pixel.get_y()) + ')'	
	
if __name__ == '__main__':
	nose.runmodule()
	
		