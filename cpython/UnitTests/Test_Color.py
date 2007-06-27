import unittest
import os.path
from TestExecute import *
from picture import *
#from media import *

# we MUST set the debug level to 1 to force errors to return
debugLevel = 1

def colorEqualsColor(color, coloro):
	# helper function to compare two colors
	return (color.get_red() == coloro.get_red() and
				color.get_green() == coloro.get_green() and
				color.get_blue() == coloro.get_blue())
	
def normalizeColor(color):
	# helper function to bound colors within [0,255]
	for idx in range(len(color)):
				color[idx] = int(color[idx]) % 256

class Test_Color(unittest.TestCase):
	''' Tests the media.py Color class members '''
			
	def tearDown(self):
		# delete the color after use
		try:
			del self.color
		except:
			done = TRUE # 			
		
	def testConstructorInvalid(self):
		# test that invalid calls to color fails
		self.assertRaises(TypeError, Color, None, None, None)
		self.assertRaises(ValueError, Color, '', '', '')

	def testConstructor(self):
		# test expectedly normal function calls
		# Color bounds to [0,255] so we must check that the new and old way are the same
		inputRGB = ( (0,0,0), (0,0,255), (255,255,255), (-1,-1,-1), (-1000, 64, 1000) )
		expectedRGB = ( (0,0,0), (0,0,255), (255,255,255), (255,255,255), (24,64,232) )
		self.failUnless(len(inputRGB) == len(expectedRGB), 'Test arrays are mapped 1:1')
		
		for idx in range(len(inputRGB)):
			r = inputRGB[idx][0]; expr = expectedRGB[idx][0]
			g = inputRGB[idx][1]; expg = expectedRGB[idx][1]
			b = inputRGB[idx][2]; expb = expectedRGB[idx][2]
			self.color = Color(r,g,b)
			self.assertEqual(self.color.r, expr, 'Invalid red color component (idx=' + str(idx) + ')')
			self.assertEqual(self.color.g, expg, 'Invalid green color component (idx=' + str(idx) + ')')
			self.assertEqual(self.color.b, expb, 'Invalid blue color component (idx=' + str(idx) + ')')
			# ensure that the old way also works (mod works differently in different languages?)
			oldRGB = [r, g, b]
			for idx in range(len(oldRGB)):
				while oldRGB[idx] < 0:
					oldRGB[idx] += 256
				while oldRGB[idx] > 255:
					oldRGB[idx] -= 256
			self.assertEqual(self.color.r, oldRGB[0], 'Invalid old red color component calc (idx=' + str(idx) + ')')
			self.assertEqual(self.color.g, oldRGB[1], 'Invalid old green color component calc (idx=' + str(idx) + ')')
			self.assertEqual(self.color.b, oldRGB[2], 'Invalid old blue color component calc (idx=' + str(idx) + ')')
			del self.color
			# test non-int inputs
			self.color = Color(str(r), str(g), str(b))
			self.assertEqual(self.color.r, expr, 'Invalid red color component (idx=' + str(idx) + ')')
			self.assertEqual(self.color.g, expg, 'Invalid green color component (idx=' + str(idx) + ')')
			self.assertEqual(self.color.b, expb, 'Invalid blue color component (idx=' + str(idx) + ')')
			del self.color
			
	def testDistance(self):		
		# test functionality for finding the euclidean distance between two colors
		colorOne = ( Color(0,0,0), Color(255,255,255), Color(0,0,255), Color(255,255,255) )
		colorTwo = ( Color(0,0,0), Color(255,255,255), Color(255,0,0), Color(0,0,0) )		
		expectedDistance = ( 0, 0, sqrt(pow(255, 2)*2), sqrt(pow(255, 2)*3) )
		self.failUnless(len(colorOne) == len(colorTwo) == len(expectedDistance), 'Test arrays are mapped 1:1')
		for idx in range(len(colorOne)):
			distanceOne = colorOne[idx].distance(colorTwo[idx])
			distanceTwo = colorTwo[idx].distance(colorOne[idx])
			self.assertEqual(distanceOne, expectedDistance[idx], 'Improper color one distance')
			self.assertEqual(distanceTwo, expectedDistance[idx], 'Improper color two distance')
			
	def testDifferenceSubtraction(self):
		# test that color subtraction works
		colorOne = ( Color(0,0,0), Color(255,255,255), Color(0,0,255), Color(255,255,255) )
		colorTwo = ( Color(0,0,0), Color(255,255,255), Color(255,0,0), Color(0,0,0) )		
		expectedDifferenceOneMinusTwo = ( Color(0,0,0), Color(0,0,0), Color(1,0,255), Color(255,255,255) )
		expectedDifferenceTwoMinusOne = ( Color(0,0,0), Color(0,0,0), Color(255,0,1), Color(1,1,1) )
		self.failUnless(len(colorOne) == len(colorTwo) == len(expectedDifferenceOneMinusTwo) == len(expectedDifferenceTwoMinusOne), 'Test arrays are mapped 1:1')
		for idx in range(len(colorOne)):
			# ensure that both difference and subtract work the same
			subOne = colorOne[idx]-colorTwo[idx]
			differenceOne = colorOne[idx].difference(colorTwo[idx])
			subTwo = colorTwo[idx]-colorOne[idx]
			differenceTwo = colorTwo[idx].difference(colorOne[idx])
			self.failUnless(colorEqualsColor(subOne, differenceOne), 'Difference and subtraction differ (one-two)')
			self.failUnless(colorEqualsColor(subTwo, differenceTwo), 'Difference and subtraction differ (two-one)')
			self.failUnless(colorEqualsColor(subOne, expectedDifferenceOneMinusTwo[idx]), 'Unexpected difference returned (one-two)')
			self.failUnless(colorEqualsColor(subTwo, expectedDifferenceTwoMinusOne[idx]), 'Unexpected difference returned (two-one)')
	
	def testSetGetRGB(self):
		# test the setters/getters of RGB components
		defaultColor = [0,0,0]
		colors = [ [1,1,1], [-1,-1,-1], [0,64,255], [255,255,255], [-10,-64,-255], [-1000,0,1000], ['10', 10, '10'] ]
		self.color = Color(defaultColor[0], defaultColor[1], defaultColor[2])
		for color in colors:
			# normalize color components
			normalizeColor(color)
			# set tuple
			self.color.set_rgb(color)
			self.assertEqual(self.color.get_rgb(), color, 'Different colors encountered after setting/getting')
			self.color.set_rgb(defaultColor)
			# set individually
			self.color.set_red(color[0])
			self.color.set_green(color[1])
			self.color.set_blue(color[2])
			self.assertEqual(self.color.get_red(), color[0], 'Different red component returned')
			self.assertEqual(self.color.get_green(), color[1], 'Different green component returned')
			self.assertEqual(self.color.get_blue(), color[2], 'Different blue component returned')
			self.color.set_rgb(defaultColor)
			
	def testMakeLighterDarker(self):
		# not quite sure how to test this other than compring the resulting color's values 
		# TODO: revisit this when we allow arbitraty changes in intensity
		colors = [ [1,1,1], [-1,-1,-1], [0,64,255], [255,255,255], [-10,-64,-255], [-1000,0,1000], ['10', 10, '10'] ]
		for color in colors:
			# normalize color components
			normalizeColor(color)
				
			cL = Color(color[0], color[1], color[2])
			cD = Color(color[0], color[1], color[2])
			cL.make_lighter()
			cD.make_darker()
			# we expect the lighter color to have values closer to white
			self.failUnless(cL.get_red() >= color[0], 'Red component is not lighter')
			self.failUnless(cL.get_green() >= color[1], 'Green component is not lighter')
			self.failUnless(cL.get_blue() >= color[2], 'Blue component is not lighter')
			# we expect the darker color to have values closer to black			
			self.failUnless(cD.get_red() <=color[0], 'Red component is not darker')
			self.failUnless(cD.get_green() <= color[1], 'Green component is not darker')
			self.failUnless(cD.get_blue() <= color[2], 'Blue component is not darker')
					
	def testToString(self):
		# ensure that tostring is returning the correct representation
		colors = [ [1,1,1], [-1,-1,-1], [0,64,255], [255,255,255], [-10,-64,-255], [-1000,0,1000], ['10', 10, '10'] ]
		for color in colors:
			# normalize color components
			normalizeColor(color)
			# compare strings
			expectedStr = 'color r=' + str(color[0]) + ' g=' + str(color[1]) + ' b=' + str(color[2])
			new_color = Color(color[0], color[1], color[2])
			self.assertEqual(str(new_color), expectedStr, 'Color strings do not match:\n' + str(new_color) + '\n' + expectedStr )
		
class Test_Color_Helpers(unittest.TestCase):
	''' Tests global functions related to the Color class '''
						
	def testNonColorObjectCall(self):
		# ensuring that all the picture global convenience functions fail on non-Picture objects
		self.assertRaises(ValueError, distance, DummyClass(), DummyClass())
		self.assertRaises(ValueError, distance, Color(0,0,0), DummyClass())
		self.assertRaises(ValueError, distance, DummyClass(), Color(0,0,0))
		self.assertRaises(ValueError, make_darker, DummyClass())
		self.assertRaises(ValueError, make_lighter, DummyClass())
		
	def testMakeNewColor(self):
		# ensure that the colors created through these are identical to those created manually
		colors = [ [1,1,1], [-1,-1,-1], [0,64,255], [255,255,255], [-10,-64,-255], [-1000,0,1000], ['10', 10, '10'] ]
		for color in colors:
			# normalize color components
			normalizeColor(color)
			# create using all three ways
			colorMake = make_color(color[0], color[1], color[2])
			colorNew = new_color(color[0], color[1], color[2])
			colorManual = Color(color[0], color[1], color[2])
			self.failUnless(colorEqualsColor(colorMake, colorNew) and colorEqualsColor(colorMake, colorManual), 'Colors not the same (' + str(colorManual) + ')')			
		
		