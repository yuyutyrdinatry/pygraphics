import unittest
import os.path
from TestExecute import *
from picture import *
#from media import *

# we MUST set the debug level to 1 to force errors to return
debugLevel = 1

def ensureImagesEqual(filenameOne, filenameTwo):
	# helper function to ensure that two image files are identical
	p1 = Picture(); p1.load_image(filenameOne)
	p2 = Picture(); p2.load_image(filenameTwo)
	ensurePicturesEqual(p1, p2)
	
def ensurePicturesEqual(p1, p2):
	# helper function to ensure that all the pixels are identical
	pixels1 = p1.get_pixels()
	pixels2 = p2.get_pixels()
	if not len(pixels1) == len(pixels2):
		raise ValueError('Improper dimensions)')
	for idx in range(len(pixels1)):
		px1 = pixels1[idx]
		px2 = pixels2[idx]
		if not (px1.get_red() == px2.get_red() and
			px1.get_green() == px2.get_green() and
			px1.get_blue() == px2.get_blue()):
			raise ValueError('Pictures not equal')
		
def ensurePicturesNotEqual(p1, p2):
	# helper function to ensure that all the pixels are identical
	pixels1 = p1.get_pixels()
	pixels2 = p2.get_pixels()
	if not len(pixels1) == len(pixels2):
		raise ValueError('Improper dimensions)')
	for idx in range(len(pixels1)):
		px1 = pixels1[idx]
		px2 = pixels2[idx]
		if not (px1.get_red() == px2.get_red() and
			px1.get_green() == px2.get_green() and
			px1.get_blue() == px2.get_blue()):
			return
	raise ValueError('Pictures equal for')	
	
def ensurePictureHasColor(picture, color):
	pixels = picture.get_pixels()
	for pixel in pixels:
		if not ((pixel.get_red() == color.get_red())
			and (pixel.get_green() == color.get_green())
			and (pixel.get_blue() == color.get_blue())):
			raise ValueError('Picture does not have solid color')

class Test_Picture(unittest.TestCase):
	''' Tests the media.py Picture class members '''
	
	# list of image types to be tested in common shared tests
	imageTypes = ['bmp', 'gif', 'jpg']
	
	def tearDown(self):
		# delete the picture after use
		try:
			del self.pict
		except:
			done = TRUE # 			
		
	def testEmptyConstructor(self):
		# empty constructor builds new picture
		self.pict = Picture()
		self.assertEqual(self.pict.disp_image, None, 'New Picture contains display image')
		self.assertEqual(self.pict.win_active, 0, 'New Picture is active')
		
	def testCreateImageZeroDimensions(self):
		# create empty image with zero dimensions
		self.pict = Picture()
		self.pict.create_image(0, 0)
		self.assertEqual(self.pict.surf.get_size(), (0, 0), "Wrong Picture dimensions")
		self.assertEqual(len(self.pict.pixels), 0, "Wrong number of Picture pixels")
		self.assertEqual(self.pict.filename, '', "Non-empty filename for empty image")
		self.assertEqual(self.pict.title, 'None', "")
		
	def testCreateImageQuestionableDimensions(self):
		# create empty image with questionable dimensions
		# TODO: should we even be creating the surface if one of the sides <= 0?
		self.pict = Picture()
		self.pict.create_image(0, 1) # what is a zero by 1 image?
		self.assertEqual(self.pict.surf.get_size(), (0, 1), "Wrong Picture dimensions")
		self.assertEqual(len(self.pict.pixels), 0, "Wrong number of Picture pixels")
		self.assertEqual(self.pict.filename, '', "Non-empty filename for empty image")
		self.assertEqual(self.pict.title, 'None', "")
		
	def testCreateImageInvalidDimensions(self):
		# create empty image with invalid dimensions
		self.pict = Picture()
		self.assertRaises(ValueError, self.pict.create_image, -1, -1)
		self.assertRaises(ValueError, self.pict.create_image, -1, 0)
		self.assertRaises(ValueError, self.pict.create_image, 0, -1)
		
	def testLoadImageNonExistantFile(self):
		# load a non-existant file
		self.pict = Picture()
		self.assertRaises(ValueError, self.pict.load_image, resi("nosuchfile"))
		
	def testLoadImage(self):
		# load a normal image file (absolute, relative)
		self.pict = Picture()
		# absolute files 
		filenamePrefix = 'white.'
		failedTest = FALSE
		# for each of the supported file types
		for suffix in self.imageTypes:
			filename = filenamePrefix + suffix
			file = resi(filename)
			# try and load the test file of that type
			try:
				self.pict.load_image(file)
				self.assertEqual(self.pict.filename, file, "Improper filename for loaded image")
				self.assertEqual(self.pict.title, os.path.join('images', filename), "Improper title for loaded image")
				# ensure correct dimensions and depth
				self.assertEqual(self.pict.surf.get_size(), (50, 50), "Invalid Picture dimensions")
				self.assertEqual(len(self.pict.pixels)*len(self.pict.pixels[0])*len(self.pict.pixels[0][0]), (50*50*3))
			except ValueError, e:
				print 'Error loading images of type: ' + suffix + " (" + str(e) + ")"
				failedTest = TRUE
		# there was at least one error loading the test files
		if failedTest:
			self.fail('Error loading image files')
		# TODO: to test relative files, we need to be able to set the global default media directory
		
	def testToStringInvalidImage(self):	
		# test toString 
		self.pict = Picture()
		# empty picture
		self.assertRaises(AttributeError, str, self.pict)
		# invalid attempt at loading picture
		self.assertRaises(ValueError, self.pict.create_image, -1, -1)
		self.assertRaises(AttributeError, str, self.pict)
		
	def testToStringDimensionlessImage(self):	
		# test toString
		self.pict = Picture()
		self.pict.create_image(0, 0)
		self.assertEqual(str(self.pict), 'Picture, filename  height 0 width 0', "Invalid toString for dimensionless image")
		
	def testToString(self):
		# test that toString is printing correct values
		self.pict = Picture()
		filenamePrefix = 'white.'
		failedTest = FALSE
		# for each of the supported file types
		for suffix in self.imageTypes:
			filename = filenamePrefix + suffix
			file = resi(filename)
			# try and load the test file of that type
			try:
				self.pict.load_image(file)
				self.assertEqual(str(self.pict), "Picture, filename " + file + " height 50 width 50", "Invalid toString")
			except ValueError, e:
				print 'Error loading images of type: ' + suffix + " (" + str(e) + ")"
				failedTest = TRUE
		# there was at least one error loading the test files
		if failedTest:
			self.fail('Error loading image files')
			
	def testTitle(self):
		# test title setters/getters
		self.pict = Picture()
		# setting after initial load
		self.assertEqual(self.pict.get_title(), 'Unnamed', "Improper initial title")
		self.pict.set_title('')
		self.assertEqual(self.pict.get_title(), '', "Improper title")
		self.pict.set_title('asdf')
		self.assertEqual(self.pict.get_title(), 'asdf', "Improper title")
		# setting after creating a new image
		self.pict.create_image(0, 0)
		self.assertEqual(self.pict.get_title(), 'None', "Improper title")
		self.pict.set_title('asdf')
		self.assertEqual(self.pict.get_title(), 'asdf', "Improper title")
		# setting after loading an image
		self.pict.load_image(resi('white.bmp'))
		self.assertEqual(self.pict.get_title(), os.path.join('images', 'white.bmp'), "Improper title")
		self.pict.set_title('asdf')
		self.assertEqual(self.pict.get_title(), 'asdf', "Improper title")
		
	def testGetImageInvalidImage(self):
		# test get_image on an invalid image
		self.pict = Picture()
		# fails when no/invalid image created
		self.assertRaises(AttributeError, self.pict.get_image)
		self.assertRaises(ValueError, self.pict.create_image, -1, -1)	# try creating invalid
		self.assertRaises(AttributeError, self.pict.get_image)
		# also seems to fail with empty image when passed into PIL
		self.pict.create_image(0, 0)
		self.assertRaises(ValueError, self.pict.get_image)
		
	def testGetImage(self):
		# ensure that the Image has the same properties as the Picture		
		# test created blank image and loaded image
		expectedColor = ((0, 0, 0), (255, 255, 255))
		for idx in range(len(expectedColor)):
			# create/load picture
			self.pict = Picture()
			if idx == 0:
				self.pict.create_image(50, 50)
			elif idx == 1:
				self.pict.load_image(resi('white.bmp'))
			# convert to PIL image and ensure properties are the same
			image = self.pict.get_image()
    		self.assertEqual(image.mode, 'RGB', "Improper image color bands")
    		self.assertEqual(image.size, (50, 50), "Improper image size")
    		# ensure all the pixels are of the correct color
    		correctColor = TRUE
    		imagePixels = list(image.getdata())
    		for pixel in imagePixels:
    			if not pixel == expectedColor[idx]:
    				correctColor = FALSE
    		if not correctColor:
    			self.fail('Invalid image colors (' + str(idx) + ')')
			del self.pict, image, imagePixels	
		
	def testGetWidthHeightInvalidImage(self):
		# test get_width/get_height for an invalid image
		self.pict = Picture()
		self.assertRaises(AttributeError, self.pict.get_width)
		self.assertRaises(AttributeError, self.pict.get_height)
		# after invalid image creation attempt
		self.assertRaises(ValueError, self.pict.create_image, -1, -1)	# try creating invalid
		self.assertRaises(AttributeError, self.pict.get_width)
		self.assertRaises(AttributeError, self.pict.get_height)
	
	def testGetWidthHeight(self):
		# test get_width/get_height for normal images
		# create image
		dimension = ((0,0), (50, 50), (0, 5), (10, 0))
		for idx in range(len(dimension)):
			self.pict = Picture()
			w = dimension[idx][0]
			h = dimension[idx][1]
			self.pict.create_image(w, h)
			self.assertEqual(self.pict.get_width(), w, 'Invalid image width')
			self.assertEqual(self.pict.get_height(), h, 'Invalid image height')
    		del self.pict
    	# load image
		self.pict = Picture()
		self.pict.load_image(resi('white.bmp'))
		self.assertEqual(self.pict.get_width(), 50, 'Invalid image width')
		self.assertEqual(self.pict.get_height(), 50, 'Invalid image height')
		
	def testGetPixelInvalidImage(self):
		# test get_pixel on an invalid image
		self.pict = Picture()
		self.assertRaises(AttributeError, self.pict.get_pixel, 0, 0)
		self.assertRaises(AttributeError, self.pict.get_pixel, -1, -1)
		self.assertRaises(AttributeError, self.pict.get_pixel, 50, 50)
		# after invalid image creation attempt
		self.assertRaises(ValueError, self.pict.create_image, -1, -1)	# try creating invalid
		self.assertRaises(AttributeError, self.pict.get_pixel, 0, 0)
		self.assertRaises(AttributeError, self.pict.get_pixel, -1, -1)
		self.assertRaises(AttributeError, self.pict.get_pixel, 50, 50)
		
	def testGetPixel(self):
		# test get_pixel on a normal image
		# NOTE: indices are ONE based
		# out of bounds indices
		self.pict = Picture()
		self.pict.create_image(0, 0)		
		self.assertRaises(IndexError, self.pict.get_pixel, 0, 0)
		self.assertRaises(IndexError, self.pict.get_pixel, -1, 0)
		self.assertRaises(IndexError, self.pict.get_pixel, -1, -1)
		self.assertRaises(IndexError, self.pict.get_pixel, 50, 50)
		del self.pict
		# single pixel image
		self.pict = Picture()
		self.pict.create_image(1, 1)		
		try:
			# should not fail
			self.pict.get_pixel(0, 0) # in python, this wraps to -1 from the left/right
			self.pict.get_pixel(1, 1) # one based index for the first pixel
		except IndexError:
			self.fail('Failed accessing expected pixel')
		self.assertRaises(IndexError, self.pict.get_pixel, 2, 2)
		del self.pict
		# multi pixel image
		self.pict = Picture()
		self.pict.create_image(10, 10)
		try:
			# should not fail
			self.pict.get_pixel(-9, -9) # last wrap around value
			self.pict.get_pixel(0, 0) # wrap around
			self.pict.get_pixel(1, 1) # first index
			self.pict.get_pixel(0, 10) 
			self.pict.get_pixel(10, 0)
			self.pict.get_pixel(10, 10) # bounds
		except IndexError:
			self.fail('Failed accessing expected pixel')
		self.assertRaises(IndexError, self.pict.get_pixel, 11, 11) # should fail
		
	def testGetPixelsInvalidImage(self):		
		# test get_pixels on invalid image
		self.pict = Picture()
		self.assertRaises(AttributeError, self.pict.get_pixels)
		# after invalid image creation attempt
		self.assertRaises(ValueError, self.pict.create_image, -1, -1)	# try creating invalid
		self.assertRaises(AttributeError, self.pict.get_pixels)
	
	def testGetPixels(self):
		# test get_pixels on a normal image
		dimensions = ((0,0), (10, 0), (0, 10), (1, 1), (10, 10))
		expectedLen = (0, 0, 0, 1, 100)
		self.failUnless(len(dimensions) == len(expectedLen), 'Test arrays are mapped 1:1')
		
		for idx in range(len(dimensions)):
			self.pict = Picture()		
    		self.pict.create_image(dimensions[idx][0], dimensions[idx][1])
    		self.assertEqual(len(self.pict.get_pixels()), expectedLen[idx], 
				'Invalid number of pixels returned (' + str(idx) + ')')    	
    		del self.pict
    	# loaded image
		self.pict = Picture()		
		self.pict.load_image(resi('white.bmp'))
		self.assertEqual(len(self.pict.get_pixels()), 50*50, 'Invalid number of pixels returned')    	
		
	def testSetPixels(self):
		# test set_pixels on an image
		self.pict = Picture()
		self.pict.create_image(44,44)
		colors = (Color(0,0,0), Color(255,0,0), Color(255,255,255))
		try:
			for color in colors:
				self.pict.set_pixels(color)
				ensurePictureHasColor(self.pict, color)
		except e, msg:
			self.fail(msg)
		
	def testClear(self):
		# test clear
		self.pict = Picture()
		self.pict.create_image(44,44)
		black = Color(0,0,0)
		colors = (Color(0,0,0), Color(255,0,0), Color(255,255,255))
		try:
			for color in colors:
				self.pict.set_pixels(color)
				self.pict.clear()
				ensurePictureHasColor(self.pict, black)
				self.pict.clear(color)
				ensurePictureHasColor(self.pict, color)
		except e, msg:
			self.fail(msg)
		
	def testWriteTo(self):
		# test that all images can be written to
		self.pict = Picture()
		blessedSaveLocPrefix = 'saved.'#resi('saved.')
		saveLocPrefix = 'saved.tmp.'#resi('saved.tmp.')
		
		# fails on invalid/empty/blank image
		self.assertRaises(AttributeError, self.pict.write_to, saveLocPrefix + 'tmp')
		self.assertRaises(ValueError, self.pict.create_image, -1, -1)	# try creating invalid
		self.assertRaises(AttributeError, self.pict.write_to, saveLocPrefix + 'tmp')
		self.pict.create_image(0, 0)
		#self.assertRaises(ValueError, self.pict.write_to, saveLocPrefix + 'tmp')
		self.assertRaises(KeyError, self.pict.write_to, saveLocPrefix + 'tmp')
		# invalid file types
		self.pict.create_image(10, 10)
		self.assertRaises(KeyError, self.pict.write_to, saveLocPrefix + 'tmp')
		# ensure all of our types hold
		for suffix in self.imageTypes:
			try:				
				self.pict.write_to(saveLocPrefix + suffix)
				# compare with saved copies
				ensureImagesEqual(blessedSaveLocPrefix + suffix, saveLocPrefix + suffix)
			except KeyError:
				self.fail('Failed saving created image to (' + suffix + ') files')
		del self.pict
		# test loaded image		
		saveLocPrefix = resi('white.tmp.')
		blessedSaveLocPrefix = resi('white.')
		for suffix in self.imageTypes:
			self.pict = Picture()
			self.pict.load_image(blessedSaveLocPrefix + suffix)
			try:
				self.pict.write_to(saveLocPrefix + suffix)
				# compare with saved copies
				ensureImagesEqual(blessedSaveLocPrefix + suffix, saveLocPrefix + suffix)
			except KeyError:
				self.fail('Failed saving loaded image to (' + suffix + ') files')
			del self.pict
							
	def testCopyFromImageInvalid(self):
		# test that copy from image fails when given bad input
		self.pict = Picture()
		p = Picture()
		p.create_image(10,10)				
		# negative coordinates
		self.assertRaises(ValueError, self.pict.copy_from_image, p, -1)
		self.assertRaises(ValueError, self.pict.copy_from_image, p, 100, -11)
		# out of bound coordinates
		self.assertRaises(ValueError, self.pict.copy_from_image, p, p.get_width()+1)
		self.assertRaises(ValueError, self.pict.copy_from_image, p, 100000000,1)
		self.assertRaises(ValueError, self.pict.copy_from_image, p, 1, 1000000)
							
	def testCopyFromImage(self):
		# test that copy from image works
		self.pict = Picture();
		p = Picture()
		p.load_image(resi('white.bmp'))
		white = Color(255,255,255)
		black = Color(0,0,0)
		# copy to self.pict whole
		dimensions = ( (None,None), (50,50), (100,100) )
		for dimen in dimensions:
			self.pict.copy_from_image(p, 1,1, dimen[0], dimen[1])
			ensurePictureHasColor(self.pict, white)
			self.assertEqual(self.pict.get_width(), 50, 'New image width not equal')			
			self.assertEqual(self.pict.get_height(), 50, 'New image height not equal')
			self.pict.clear()
		# copy sub image
		coordinates = ( (1,1), (4,4), (6,6), (1,2), (3,4) )
		dimensions = ( (2,2), (2,2), (2,2), (1,4), (6,2) )
		self.failUnless(len(coordinates) == len(dimensions), 'Test arrays are mapped 1:1')
		for idx in range(len(coordinates)):
			self.pict.copy_from_image(p, coordinates[idx][0],coordinates[idx][1], dimensions[idx][0], dimensions[idx][1])
			ensurePictureHasColor(self.pict, white)
			self.assertEqual(self.pict.get_width(), dimensions[idx][0], 'New image width not equal')			
			self.assertEqual(self.pict.get_height(), dimensions[idx][1], 'New image height not equal')
			self.pict.clear()		
		
	def testGetPictureWithHeight(self):
		# TODO
		print "TBD"
	
	def testLoadAndShowPicture(self):
		# TODO
		print "TBD"
	
	def testGetTransformEnclosingRect(self):
		# TODO
		print "TBD"	
	
	
class Test_Picture_Helpers(unittest.TestCase):
	''' Tests global functions related to the Picture class '''
		
	def testMakePictureInvalidFile(self):
		# test invalid case
		imageLoc = resi('doesNotExist.img')
		self.assertRaises(ValueError, make_picture, imageLoc)
		
	def testMakePicture(self):
		# ensure that this returns an identical picture from one created manually
		imageLoc = resi('white.bmp')
		pMP = make_picture(imageLoc)
		pManual = Picture(); pManual.load_image(imageLoc)
		ensurePicturesEqual(pMP, pManual)
				
	def testNonPictureObjectCall(self):
		# ensuring that all the picture global convenience functions fail on non-Picture objects
		self.assertRaises(ValueError, get_pixel, DummyClass(), 0, 0)
		self.assertRaises(ValueError, get_pixels, DummyClass())
		self.assertRaises(ValueError, get_width, DummyClass())
		self.assertRaises(ValueError, get_height, DummyClass())
		self.assertRaises(ValueError, show, DummyClass())
		self.assertRaises(ValueError, repaint, DummyClass())
		self.assertRaises(ValueError, add_line, DummyClass(), 0, 0, 0, 0)
		self.assertRaises(ValueError, add_text, DummyClass(), 0, 0, '')
		self.assertRaises(ValueError, add_rect, DummyClass(), 0, 0, 0, 0)
		self.assertRaises(ValueError, add_rect_filled, DummyClass(), 0, 0, 0, 0, None)
		self.assertRaises(ValueError, write_picture_to, DummyClass(), '')
		self.assertRaises(ValueError, duplicate_picture, DummyClass())
		self.assertRaises(ValueError, set_pixels, DummyClass(), None)
		self.assertRaises(ValueError, set_pixels, Picture(), DummyClass())
		
	def testDuplicatePicture(self):
		# ensure that the new picture is equal to the old picture
		imageLoc = resi('white.bmp')
		self.pict = Picture()
		self.pict.load_image(imageLoc)
		# copy full image
		p = duplicate_picture(self.pict)
		ensurePicturesEqual(self.pict, p)
		# ensure that changing one does not affect the other
		self.pict.clear();
		ensurePicturesNotEqual(self.pict, p)
				
	def testGetShortPath(self):
		# ensure that the short path is returned correctly
		self.assertEqual(get_short_path(''), '', 'Invalid short path')
		self.assertEqual(get_short_path('a.img'), 'a.img', 'Invalid short path')
		self.assertEqual(get_short_path(os.path.join('b', 'a.img')), os.path.join('b', 'a.img'), 'Invalid short path')
		self.assertEqual(get_short_path(os.path.join('c', os.path.join('b', 'a.img'))), os.path.join('b', 'a.img'), 'Invalid short path')


