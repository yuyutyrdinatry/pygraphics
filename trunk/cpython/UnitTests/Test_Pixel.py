import unittest
import os.path
from TestExecute import *
from picture import *
#from media import *

# we MUST set the debug level to 1 to force errors to return
debugLevel = 1

def pixelEqualsColor(pixel, color):
	# helper function to compare pixel and color values
	return (pixel.get_red() == color.get_red() and
				pixel.get_green() == color.get_green() and
				pixel.get_blue() == color.get_blue())

def pixelEqualsColorArray(pixel, array3d):
	# helper function to compare pixel color values
	return (pixel.get_red() == array3d[0] and
		pixel.get_green() == array3d[1] and
		pixel.get_blue() == array3d[2])
	
def pixelXYEqualsArray(pixel, array2d):
	# helper function to compare pixel coordinates
	return (pixel.get_x() == array2d[0] and pixel.get_y() == array2d[1])
	
def colorEqualsColor(color, coloro):
	# helper function to compare two colors
	return (color.get_red() == coloro.get_red() and
				color.get_green() == coloro.get_green() and
				color.get_blue() == coloro.get_blue())

class Test_Pixel(unittest.TestCase):
	''' Tests the media.py Pixel class members '''
	
	B = [0,0,0]
	W = [255,255,255]
	img =	[[B, W], \
				[W, B]]	
	largeImg = [	[B, W, B, W], \
							[W, B, W, B], \
							[B, W, B, W], \
							[W, B, W, B]	]
		
	def tearDown(self):
		# delete the pixel after use
		try:
			del self.pixel
		except:
			done = TRUE # 			
		
	def testConstructorInvalid(self):
		# test that invalid calls to pixel fails
		# NOTE: pixels is of type [x=[y=[RGB]]], and x,y are ONE based
		self.assertRaises(TypeError, Pixel, None, 0, 0)
		self.assertRaises(IndexError, Pixel, [], 0, 0)
		self.assertRaises(ValueError, Pixel, [[]], 0, 0)
		self.assertRaises(IndexError, Pixel, [[1], [1]], -10, 10) # exceeds wrap-around bounds
		
	def testConstructor(self):
		# test the constructor		
		try:
			# could loop this, but in this case, it makes it easier to understand
			self.pixel = Pixel(self.img, 1, 1) # x=0, y=0
			self.assertEqual(self.pixel.x, 0, 'Invalid x coordinate')
			self.assertEqual(self.pixel.y, 0, 'Invalid y coordinate')
			self.assertEqual(self.pixel.pix, self.B, 'Invalid pixel color')
			del self.pixel
			self.pixel = Pixel(self.img, 2, 1) # x=1, y=0
			self.assertEqual(self.pixel.x, 1, 'Invalid x coordinate')
			self.assertEqual(self.pixel.y, 0, 'Invalid y coordinate')
			self.assertEqual(self.pixel.pix, self.W, 'Invalid pixel color')
			del self.pixel
			self.pixel = Pixel(self.img, 1, 2) # x=0, y=1
			self.assertEqual(self.pixel.x, 0, 'Invalid x coordinate')
			self.assertEqual(self.pixel.y, 1, 'Invalid y coordinate')
			self.assertEqual(self.pixel.pix, self.W, 'Invalid pixel color')
			del self.pixel
			self.pixel = Pixel(self.img, 2, 2) # x=1, y=1
			self.assertEqual(self.pixel.x, 1, 'Invalid x coordinate')
			self.assertEqual(self.pixel.y, 1, 'Invalid y coordinate')
			self.assertEqual(self.pixel.pix, self.B, 'Invalid pixel color')
			del self.pixel
			# wraparound
			self.pixel = Pixel(self.img, 0, 0) # x=1, y=1
			self.assertEqual(self.pixel.x, 1, 'Invalid x coordinate')
			self.assertEqual(self.pixel.y, 1, 'Invalid y coordinate')
			self.assertEqual(self.pixel.pix, self.B, 'Invalid pixel color')
			del self.pixel
			self.pixel = Pixel(self.img, 0, -1) # x=1, y=0
			self.assertEqual(self.pixel.x, 1, 'Invalid x coordinate')
			self.assertEqual(self.pixel.y, 0, 'Invalid y coordinate')
			self.assertEqual(self.pixel.pix, self.W, 'Invalid pixel color')
			del self.pixel
			self.pixel = Pixel(self.img, -1, 0) # x=0, y=1
			self.assertEqual(self.pixel.x, 0, 'Invalid x coordinate')
			self.assertEqual(self.pixel.y, 1, 'Invalid y coordinate')
			self.assertEqual(self.pixel.pix, self.W, 'Invalid pixel color')
			del self.pixel
			self.pixel = Pixel(self.img, -1, -1) # x=0, y=0
			self.assertEqual(self.pixel.x, 0, 'Invalid x coordinate')
			self.assertEqual(self.pixel.y, 0, 'Invalid y coordinate')
			self.assertEqual(self.pixel.pix, self.B, 'Invalid pixel color')
			del self.pixel
		except:
			self.fail('Failed on proper constructor')
				
	def testSetGetRGB(self):
		# test that setters and getters for RGB are working
		# TODO: also test for Alpha if we add support for that
		self.pixel = Pixel(self.img, 1, 1)
		
		self.failUnless(pixelEqualsColorArray(self.pixel, self.B), 'Improper color component')
		self.pixel.setRed(0) # empty set
		self.pixel.set_green(0)
		self.pixel.set_blue(0)
		self.failUnless(pixelEqualsColorArray(self.pixel, self.B), 'Improper color component')
		self.pixel.setRed(255) # set new red
		self.failUnless(pixelEqualsColorArray(self.pixel, [255, 0, 0]), 'Improper color component')
		self.pixel.set_blue(128) # set new blue
		self.failUnless(pixelEqualsColorArray(self.pixel, [255, 0, 128]), 'Improper color component')
		self.pixel.set_green(64) # set green
		self.failUnless(pixelEqualsColorArray(self.pixel, [255, 64, 128]), 'Improper color component')
		self.pixel.set_blue(255); self.pixel.set_green(255)
		self.failUnless(pixelEqualsColorArray(self.pixel, self.W), 'Improper color component')
		# test out of bounds color values
		outOfBounds = [-1, -10, 256, 300]
		for value in outOfBounds:
			self.assertRaises(ValueError, self.pixel.setRed, value)
			self.assertRaises(ValueError, self.pixel.set_green, value)
			self.assertRaises(ValueError, self.pixel.set_blue, value)
		
	def testSetGetColor(self):
		# test that setters and getters for pixel color is correct
		colors = (Color(0, 0, 0), Color(-1, -1, -1), Color(0, 64, 32), Color(255, 255, 255))
		self.pixel = Pixel(self.img, 1, 1)
		for color in colors:
			# ensure that the colors are the same after setting and getting
			self.pixel.set_color(color)
			self.failUnless(pixelEqualsColor(self.pixel, color), 'Colors do not match (' + str(self.pixel) + ', ' + str(color) + ')')
			self.failUnless(colorEqualsColor(self.pixel.get_color(), color), 'Colors do not match (' + str(self.pixel.get_color()) + ', ' + str(color) + ')')

	def testGetXY(self):
		# test that get_x and get_y return valid indices within ranges x=[0, width], y=[0, height]
		width = len(self.largeImg)
		height = len(self.largeImg[0])
		
		inputCoordinates = ((1, 1), (4, 4), (0, 0), (-1, -1), (-2, -2), (-3, -3))
		expectedCoordinates = ((1, 1), (4, 4), (4, 4), (3, 3), (2, 2), (1, 1))	# wrap around values will be bounded
		self.failUnless(len(inputCoordinates) == len(expectedCoordinates), 'Test arrays are mapped 1:1')
		# test each of the input coordinates, making sure they map to the correct expected coords
		for idx in range(len(inputCoordinates)):
			self.pixel = Pixel(self.largeImg, inputCoordinates[idx][0], inputCoordinates[idx][1])
			self.failUnless(pixelXYEqualsArray(self.pixel, expectedCoordinates[idx]), 'Improper XY coordinates (' + str(self.pixel.get_x()) + ', ' + str(self.pixel.get_y()) + ')')			
			del self.pixel
		
class Test_Pixel_Helpers(unittest.TestCase):
	''' Tests global functions related to the Pixel class '''
						
	def testNonPixelObjectCall(self):
		# ensuring that all the picture global convenience functions fail on non-Picture objects
		self.assertRaises(ValueError, set_red, DummyClass(), 0)
		self.assertRaises(ValueError, set_green, DummyClass(), 0)
		self.assertRaises(ValueError, set_blue, DummyClass(), 0)
		self.assertRaises(ValueError, get_red, DummyClass())
		self.assertRaises(ValueError, get_green, DummyClass())
		self.assertRaises(ValueError, get_blue, DummyClass())
		self.assertRaises(ValueError, get_color, DummyClass())
		self.assertRaises(ValueError, set_color, DummyClass(), None)
		self.assertRaises(ValueError, set_color, Pixel([[0,0,0]], 1, 1), None)
		self.assertRaises(ValueError, get_x, DummyClass())
		self.assertRaises(ValueError, get_y, DummyClass())
		
		