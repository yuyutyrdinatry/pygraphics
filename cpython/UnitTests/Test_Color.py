import unittest
import os.path
from TestExecute import *
from picture import *
#from media import *

# Convention Concerns:
	# unittest uses different conventions than we are implementing (i.e. camelCase). 
	# Do we ignore? Do we worry about inconsistency?

# we MUST set the debug level to 1 to force errors to return
debugLevel = 1

# Perhaps reserve the variable name "color" for Color objects?
	# Option: color_array for RGB lists, others?
	
def normalize_color_array(color_array):
	'''Normalize list color_array to bound values within [0, 255].
	
	Note: color_array is intended to be a list with int values R, G, B in the following format, [R, G, B]'''
	
	for idx in range(len(color_array)):
				color_array[idx] = int(color_array[idx]) % 256

class TestColor(unittest.TestCase):
	''' Tests the picture.py Color class members '''
		
	def test_constructor_invalid(self):
		'''Test that Color constructor fails with invalid RGB value input.'''
		self.assertRaises(TypeError, Color, None, None, None)
		self.assertRaises(ValueError, Color, '', '', '')

	def test_constructor(self):
		'''Test Color constructor. Particularly, that it accepts normalized [0, 255] RGB values, 
		non-normalized values (e.g. 1000), and str values (e.g. "1")'''
		# test expectedly normal function calls
		# Color bounds to [0,255] so we must check that the new and old way are the same
		input_RGB = ( (0,0,0), (0,0,255), (255,255,255), (-1,-1,-1), (-1000, 64, 1000) )
		expected_RGB = ( (0,0,0), (0,0,255), (255,255,255), (255,255,255), (24,64,232) )
		self.failUnless(len(input_RGB) == len(expected_RGB), 'Test arrays are mapped 1:1')
		
		for idx in range(len(input_RGB)):
			r = input_RGB[idx][0]; expr = expected_RGB[idx][0]
			g = input_RGB[idx][1]; expg = expected_RGB[idx][1]
			b = input_RGB[idx][2]; expb = expected_RGB[idx][2]
			tester_color = Color(r,g,b)
			self.assertEqual(tester_color.r, expr, 'Invalid red color component (idx=' + str(idx) + ')')
			self.assertEqual(tester_color.g, expg, 'Invalid green color component (idx=' + str(idx) + ')')
			self.assertEqual(tester_color.b, expb, 'Invalid blue color component (idx=' + str(idx) + ')')
			# ensure that the old way also works (mod works differently in different languages?)
			oldRGB = [r, g, b]
			for idx in range(len(oldRGB)):
				while oldRGB[idx] < 0:
					oldRGB[idx] += 256
				while oldRGB[idx] > 255:
					oldRGB[idx] -= 256
			self.assertEqual(tester_color.r, oldRGB[0], 'Invalid old red color component calc (idx=' + str(idx) + ')')
			self.assertEqual(tester_color.g, oldRGB[1], 'Invalid old green color component calc (idx=' + str(idx) + ')')
			self.assertEqual(tester_color.b, oldRGB[2], 'Invalid old blue color component calc (idx=' + str(idx) + ')')

			# test non-int inputs
			tester_color = Color(str(r), str(g), str(b))
			self.assertEqual(tester_color.r, expr, 'Invalid red color component (idx=' + str(idx) + ')')
			self.assertEqual(tester_color.g, expg, 'Invalid green color component (idx=' + str(idx) + ')')
			self.assertEqual(tester_color.b, expb, 'Invalid blue color component (idx=' + str(idx) + ')')
			
	def test_eq(self):
		'''Test the __eq__ method of Color'''
		colors1 = [Color(0,0,0), Color(255, 255, 255), Color(50, 50, 50)]
		colors2 = [Color(0,0,0), Color(255, 255, 255), Color(50, 50, 50)]
		for idx in range(len(colors1)):
			self.failUnless(colors1[idx] == colors2[idx])

	
	def test_distance(self):
		'''Test distance method for finding the euclidean distance between two colors.'''		
		colors1 = ( Color(0,0,0), Color(255,255,255), Color(0,0,255), Color(255,255,255) )
		colors2 = ( Color(0,0,0), Color(255,255,255), Color(255,0,0), Color(0,0,0) )		
		expected_distance = ( 0, 0, sqrt(pow(255, 2)*2), sqrt(pow(255, 2)*3) )
		self.failUnless(len(colors1) == len(colors2) == len(expected_distance), 'Test arrays are mapped 1:1')
		for idx in range(len(colors1)):
			distance1 = colors1[idx].distance(colors2[idx])
			distance2 = colors2[idx].distance(colors1[idx])
			self.assertEqual(distance1, expected_distance[idx], 'Improper color one distance')
			self.assertEqual(distance2, expected_distance[idx], 'Improper color two distance')
			
	def test_difference_subtraction(self):
		'''Test Color subtraction and difference methods.'''
		# test that color subtraction works
		colors1 = ( Color(0,0,0), Color(255,255,255), Color(0,0,255), Color(255,255,255) )
		colors2 = ( Color(0,0,0), Color(255,255,255), Color(255,0,0), Color(0,0,0) )		
		expected_difference_one_minus_two = ( Color(0,0,0), Color(0,0,0), Color(1,0,255), Color(255,255,255) )
		expected_difference_two_minus_one = ( Color(0,0,0), Color(0,0,0), Color(255,0,1), Color(1,1,1) )
		self.failUnless(len(colors1) == len(colors2) == len(expected_difference_one_minus_two) == len(expected_difference_two_minus_one), 'Test arrays are mapped 1:1')
		for idx in range(len(colors1)):
			# ensure that both difference and subtract work the same
			sub1 = colors1[idx]-colors2[idx]
			difference1 = colors1[idx].difference(colors2[idx])
			sub2 = colors2[idx]-colors1[idx]
			difference2 = colors2[idx].difference(colors1[idx])
			self.failUnless(sub1 == difference1, 'Difference and subtraction differ (one-two)')
			self.failUnless(sub2 == difference2, 'Difference and subtraction differ (two-one)')
			self.failUnless(sub1 == expected_difference_one_minus_two[idx], 'Unexpected difference returned (one-two)')
			self.failUnless(sub2 == expected_difference_two_minus_one[idx], 'Unexpected difference returned (two-one)')
	
	def test_set_get_RGB(self):
		'''Test setting and getting RGB values from Color object.'''
		# test the setters/getters of RGB components
		default_color = [0,0,0]
		color_arrays = [ [1,1,1], [-1,-1,-1], [0,64,255], [255,255,255], [-10,-64,-255], [-1000,0,1000], ['10', 10, '10'] ]
		tester_color = Color(default_color[0], default_color[1], default_color[2])
		for color_array in color_arrays:
			# normalize color components
			normalize_color_array(color_array)
			# set tuple
			tester_color.set_rgb(color_array)
			self.assertEqual(tester_color.get_rgb(), color_array, 'Different colors encountered after setting/getting')
			tester_color.set_rgb(default_color)
			# set individually
			tester_color.set_red(color_array[0])
			tester_color.set_green(color_array[1])
			tester_color.set_blue(color_array[2])
			self.assertEqual(tester_color.get_red(), color_array[0], 'Different red component returned')
			self.assertEqual(tester_color.get_green(), color_array[1], 'Different green component returned')
			self.assertEqual(tester_color.get_blue(), color_array[2], 'Different blue component returned')
			tester_color.set_rgb(default_color)
			
	def test_make_lighter_darker(self):
		'''Test make_lighter and make_darker methods of Color object.'''
		# not quite sure how to test this other than comparing the resulting color's values 
		# TODO: revisit this when we allow arbitrary changes in intensity
		color_arrays = [ [1,1,1], [-1,-1,-1], [0,64,255], [255,255,255], [-10,-64,-255], [-1000,0,1000], ['10', 10, '10'] ]
		for color_array in color_arrays:
			# normalize color components
			normalize_color_array(color_array)
				
			cL = Color(color_array[0], color_array[1], color_array[2])
			cD = Color(color_array[0], color_array[1], color_array[2])
			cL.make_lighter()
			cD.make_darker()
			# we expect the lighter color to have values closer to white
			self.failUnless(cL.get_red() >= color_array[0], 'Red component is not lighter')
			self.failUnless(cL.get_green() >= color_array[1], 'Green component is not lighter')
			self.failUnless(cL.get_blue() >= color_array[2], 'Blue component is not lighter')
			# we expect the darker color to have values closer to black			
			self.failUnless(cD.get_red() <= color_array[0], 'Red component is not darker')
			self.failUnless(cD.get_green() <= color_array[1], 'Green component is not darker')
			self.failUnless(cD.get_blue() <= color_array[2], 'Blue component is not darker')
					
	def test_to_string(self):
		'''Test __str__ method of Color object.'''
		color_arrays = [ [1,1,1], [-1,-1,-1], [0,64,255], [255,255,255], [-10,-64,-255], [-1000,0,1000], ['10', 10, '10'] ]
		for color_array in color_arrays:
			# normalize color components
			normalize_color_array(color_array)
			# compare strings
			expected_str = 'color r=' + str(color_array[0]) + ' g=' + str(color_array[1]) + ' b=' + str(color_array[2])
			new_color = Color(color_array[0], color_array[1], color_array[2])
			self.assertEqual(str(new_color), expected_str, 'Color strings do not match:\n' + str(new_color) + '\n' + expected_str )
		
class TestColorHelpers(unittest.TestCase):
	''' Tests global functions related to the Color class '''
						
	def test_non_color_object_call(self):
		'''Test whether various Color object methods raise appropriate errors when called on non-Color objects.'''
		self.assertRaises(ValueError, distance, DummyClass(), DummyClass())
		self.assertRaises(ValueError, distance, Color(0,0,0), DummyClass())
		self.assertRaises(ValueError, distance, DummyClass(), Color(0,0,0))
		self.assertRaises(ValueError, make_darker, DummyClass())
		self.assertRaises(ValueError, make_lighter, DummyClass())
		
	def test_make_new_color(self):
		'''Test picture module functions make_color and new_color to ensure they create Color objects identical to ones created manually.'''
		color_arrays = [ [1,1,1], [-1,-1,-1], [0,64,255], [255,255,255], [-10,-64,-255], [-1000,0,1000], ['10', 10, '10'] ]
		for color_array in color_arrays:
			# normalize color components
			normalize_color_array(color_array)
			# create using all three ways
			color_make = make_color(color_array[0], color_array[1], color_array[2])
			color_new = new_color(color_array[0], color_array[1], color_array[2])
			color_manual = Color(color_array[0], color_array[1], color_array[2])
			self.failUnless(color_make == color_new and color_make == color_manual, 'Colors not the same (' + str(color_manual) + ')')			
		
		