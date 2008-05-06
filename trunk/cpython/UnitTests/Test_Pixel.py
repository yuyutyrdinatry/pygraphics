#import unittest
#import os.path
#from TestExecute import *
from picture import *
import nose
#from media import *

###############################################################################
# Module global variables
##############################################################################

_black_array = [0,0,0]
_white_array = [255,255,255]
_black_tuple = tuple(_black_array)
_white_tuple = tuple(_white_array)
_img = Picture()	
_large_img = Picture()

###############################################################################
# Setup function
##############################################################################

def setup_function():
	'''A setup function to be called by nose at the beginning of every test.'''
	# set up a small picture
	_img.surf = Image.new("RGB",(2,2))
	_img.surf.putdata([_black_tuple,_white_tuple,_white_tuple,_black_tuple])
	_img.pixels = _img.surf.load()
	# set up the larger picture
	_large_img.surf = Image.new("RGB",(4,4))
	_large_img.surf.putdata([_black_tuple,_white_tuple,_black_tuple,_white_tuple,\
							 _white_tuple,_black_tuple,_white_tuple,_black_tuple,\
							 _black_tuple,_white_tuple,_black_tuple,_white_tuple,\
							 _white_tuple,_black_tuple,_white_tuple,_black_tuple,])
	_large_img.pixels = _large_img.surf.load()

###############################################################################
# Test functions
##############################################################################

@nose.with_setup(setup_function)
def test_constructor_invalid():
	'''Test the constructor of Pixel on improper input, Errors expected.'''
	# NOTE: pixels is of type [x=[y=[RGB]]], and x,y are ONE based
	try:
		p = Pixel(None, 0, 0)
		assert False, "None as Picture in Pixel construction: Exception not raised."
	except ValueError:
		assert True
	except Exception, e:
		assert False, "None as Picture in Pixel construction: The wrong exception" + repr(e) + "was raised."
	
	try:
		p = Pixel(_img, 0, 0)
		assert True, "0 as coordinate in Pixel construction: Exception not raised."
	except IndexError:
		assert False, "0 as coordinate in Pixel construction: IndexError raised."
	except Exception, e:
		assert False, "0 as coordinate in Pixel construction: The wrong exception" + repr(e) + "was raised."

	try:
		p = Pixel(_img, 2, 2)
		assert False, "Off by one as coordinate in Pixel construction: Exception not raised."
	except IndexError:
		assert True
	except Exception, e:
		assert False, "Off by one as coordinate in Pixel construction: The wrong exception" + repr(e) + "was raised."

	try:
		p = Pixel(_img, -10, 10)
		assert False, "Wrap-around bounds exceeded in Pixel construction: Exception not raised."
	except IndexError:
		assert True
	except Exception, e:
		assert False, "Wrap-around bounds exceeded in Pixel construction: The wrong exception" + repr(e) + "was raised."

@nose.with_setup(setup_function)
def test_constructor():
	'''Test the constructor of Pixel on proper input.'''
	try:
		#positive pixel coordinates
		for x in range(_img.surf.size[0]):
			for y in range(_img.surf.size[1]):
				tester_pixel = Pixel(_img, x, y) # x=0, y=0
				assert tester_pixel.x == x, 'Invalid x coordinate initialized'
				assert tester_pixel.y == y, 'Invalid y coordinate initialized'
				if x == y:
					assert list(tester_pixel.pix.pixels[tester_pixel.x,tester_pixel.y]) == _black_array, 'Invalid pixel color initialized'
				else:
					assert list(tester_pixel.pix.pixels[tester_pixel.x,tester_pixel.y]) == _white_array, 'Invalid pixel color initialized'
		#warparound coordinates
		for x in range(0, -_img.surf.size[0], -1):
			for y in range(0, _img.surf.size[1], -1):
				tester_pixel = Pixel(_img, x, y) # x=0, y=0
				assert tester_pixel.x == abs(x), 'Invalid x coordinate initialized'
				assert tester_pixel.y == abs(y), 'Invalid y coordinate initialized'
				if x == y:
					assert list(tester_pixel.pix.pixels[tester_pixel.x,tester_pixel.y]) == _black_array, 'Invalid pixel color initialized'
				else:
					assert list(tester_pixel.pix.pixels[tester_pixel.x,tester_pixel.y]) == _white_array, 'Invalid pixel color initialized'
	
	except:
		assert False, "Failed on proper construction input."

@nose.with_setup(setup_function)
def test_has_color():
	'''Test the has_color and has_color_values methods of Pixel.'''
	tester_pixel = Pixel(_img, 0, 0)
	tester_color_arrays = [(0, 0, 0), (255, 255, 255), (128, 128, 128)]
	for color_array in tester_color_arrays:
		tester_pixel.pix.pixels[tester_pixel.x, tester_pixel.y] = color_array
		tester_color = Color(0,0,0)
		tester_color.set_rgb(color_array)
		assert tester_pixel.has_color(tester_color), "has_color failed on proper Color input"
		assert tester_pixel.has_color_values(color_array), "has_color_value failed on proper value input"

@nose.with_setup(setup_function)
def test_set_RGB_inbounds():
	'''Test setting RGB values for Pixel.'''
	# TODO: also test for Alpha if we add support for that
	tester_pixel = Pixel(_img, 0, 0)
	assert tester_pixel.has_color_values(_black_array), 'Improper color component, should be [0, 0, 0]'
	tester_pixel.set_red(0) # empty set
	tester_pixel.set_green(0)
	tester_pixel.set_blue(0)
	assert tester_pixel.has_color_values(_black_array), 'Improper color component, should be [0, 0, 0]'
	tester_pixel.set_red(255) # set new red
	assert tester_pixel.has_color_values([255, 0, 0]), 'Improper color component, should be [255, 0, 0]'
	tester_pixel.set_blue(128) # set new blue
	assert tester_pixel.has_color_values([255, 0, 128]), 'Improper color component, should be [255, 0, 128]'
	tester_pixel.set_green(64) # set green
	assert tester_pixel.has_color_values([255, 64, 128]), 'Improper color component, should be [255, 64, 128]'
	tester_pixel.set_blue(255); tester_pixel.set_green(255)
	assert tester_pixel.has_color_values(_white_array), 'Improper color component, should be [255, 255, 255]'

@nose.with_setup(setup_function)
def test_set_RGB_outbounds():
	outbounds = [-1, -10, 256, 300]
	tester_pixel = Pixel(_img, 0, 0)
	for value in outbounds:
		try:
			tester_pixel.set_red(value)
			assert False, "Out of bounds color value %d in set_red: Exception not raised." % value
		except ValueError:
			assert True
		except Exception, e:
			assert False, "Out of bounds color value %d in set_red: The wrong exception" + repr(e) + "was raised." % value

		try:
			tester_pixel.set_green(value)
			assert False, "Out of bounds color value %d in set_green: Exception not raised." % value
		except ValueError:
			assert True
		except Exception, e:
			assert False, "Out of bounds color value %d in set_green: The wrong exception" + repr(e) + "was raised." % value

		try:
			tester_pixel.set_blue(value)
			assert False, "Out of bounds color value %d in set_blue: Exception not raised." % value
		except ValueError:
			assert True
		except Exception, e:
			assert False, "Out of bounds color value %d in set_blue: The wrong exception" + repr(e) + "was raised." % value

@nose.with_setup(setup_function)
def test_get_RGB():
	'''Test getting Pixel RGB values methods.'''
	tester_pixel = Pixel(_img, 0, 0)
	assert tester_pixel.has_color_values(_black_array), 'Improper color gotten'
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

@nose.with_setup(setup_function)
def test_set_get_color():
	'''Test the setting and getting Color for Pixel.'''
	colors = [Color(0, 0, 0), Color(-1, -1, -1), Color(0, 64, 32), Color(255, 255, 255)]
	tester_pixel = Pixel(_img, 0, 0)
	for color in colors:
		# ensure that the colors are the same after setting and getting
		tester_pixel.set_color(color)
		assert tester_pixel.has_color(color), 'Colors do not match (' + str(tester_pixel) + ', ' + str(color) + ')'
		assert tester_pixel.get_color() == color, 'Colors do not match (' + str(tester_pixel.get_color()) + ', ' + str(color) + ')'

@nose.with_setup(setup_function)
def test_has_XY():
	'''Test the has_XY method of Pixel.'''
	len_x = _large_img.surf.size[0]
	len_y = _large_img.surf.size[1]
	
	# test in range x, y
	for x in range(len_x):
		for y in range(len_y):
			tester_pixel = Pixel(_large_img, x, y)
			assert tester_pixel.has_XY(x, y), "has_XY failed on proper in-bound input"
			
	# test out of range x, y (IndexError expected)
	for x in range(len_x, len_x * 2):
		for y in range(len_y, len_y * 2):
			tester_pixel = Pixel(_large_img, x % len_x, y % len_y)
			try:
				tester_pixel.has_XY(x, y)
				assert False, "Out of bounds coordinates (%d, %d) in has_XY: Exception not raised." % (x, y)
			except IndexError:
				assert True
			except Exception, e:
				assert False, "Out of bounds coordinates (%d, %d) in has_XY: The wrong exception" + repr(e) + "was raised." % (x, y)

@nose.with_setup(setup_function)
def test_get_XY():
	'''Test that get_x and get_y return valid indices within ranges x=[0, width], y=[0, height]'''
	width = _large_img.get_width()
	height = _large_img.get_height()
	
	input_coordinates = [(0, 0), (3, 3), (-1, -1), (-2, -2), (-3, -3)]
	expected_coordinates = [(0, 0), (3, 3), (3, 3), (2, 2), (1, 1)]	# wrap around values will be bounded
	assert len(input_coordinates) == len(expected_coordinates), 'Test arrays are not mapped 1:1'
	# test each of the input coordinates, making sure they map to the correct expected coords
	for idx in range(len(input_coordinates)):
		tester_pixel = Pixel(_large_img, input_coordinates[idx][0], input_coordinates[idx][1])
		assert tester_pixel.has_XY(expected_coordinates[idx][0], expected_coordinates[idx][1]), 'Improper XY coordinates (' + str(tester_pixel.get_x()) + ', ' + str(tester_pixel.get_y()) + ')'	

#Superfluous?
#def non_pixel_object_call():
#	'''Test that Pixel methods called on non-Pixel class raise appropriate ValueError.'''
#	self.init()
#	# ensuring that all the picture global convenience functions fail on non-Picture objects
#	self.assertRaises(ValueError, set_red, DummyClass(), 0)
#	self.assertRaises(ValueError, set_green, DummyClass(), 0)
#	self.assertRaises(ValueError, set_blue, DummyClass(), 0)
#	self.assertRaises(ValueError, get_red, DummyClass())
#	self.assertRaises(ValueError, get_green, DummyClass())
#	self.assertRaises(ValueError, get_blue, DummyClass())
#	self.assertRaises(ValueError, get_color, DummyClass())
#	self.assertRaises(ValueError, set_color, DummyClass(), None)
#	self.assertRaises(ValueError, set_color, Pixel(_img, 1, 1), None)
#	self.assertRaises(ValueError, get_x, DummyClass())
#	self.assertRaises(ValueError, get_y, DummyClass())
	
if __name__ == '__main__':
	nose.runmodule()
	
		