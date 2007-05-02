#
# Media Wrappers for "Introduction to Media Computation"
# Started: Mark Guzdial, 2 July 2002
#
# 7 December Lots of new stuff
#		dumped wxwindows because it hates threads and really despises pygame
#		tkinter used as alternative this is python standard for windowing
#		add PIL as a requirement to allow for easy image export and save to jpeg
#		converted pickAFile, pickAFolder, pickAColor to TKDialog pop-ups
#		moved initialization out of the class init and into the main import
#
# NOTE:
#		due to issues with Tkinter and PyGame, we can not initialize pygame.display
#		without	causing Tkinter dialogs to mess up.  For the time being,
#		pygame.display should not be initialized (all the other functions work,
#		ie. with pygame.surface).  If you run into code which requires
#		pygame.display to be initialized, please find an alternative.
#
#		- (surface.convert requires pygame.display to be inited and should not
#			be used, use the PIL Image module instead)
#

from Image import fromstring
from math import sqrt
from Queue import *
from threading import *
from Tkinter import *
from tkCommonDialog import Dialog
import cStringIO
import Image
import ImageTk
import inspect
import Numeric
import os
import pygame
import re
import struct
import sys
import thread
import time
import tkColorChooser
import tkFileDialog
import tkMessageBox
import tkSnack
import user

##
## Global vars -------------------------------------------------------
##
ver = "1.1"
defaultFrequency = 22050
defaultSampleSize = -16 		# negative denotes signed number of bits
defaultNumChannels = 1		# stereo or mono
pygame.mixer.pre_init(defaultFrequency, defaultSampleSize, (defaultNumChannels > 1))
pygame.font.init()
pygame.mixer.init()
defaultFont = pygame.font.SysFont("times", 24)

top = Tk()
top.withdraw()
# set up the tkSnack sound library
tkSnack.initializeSnack(top)

mediaFolder = user.home + os.sep

##
## Global misc functions -------------------------------------------------------
##
def version():
	global ver
	return ver

def setMediaPath():
	global mediaFolder
	file = pickAFolder()
	mediaFolder = file
	print "New media folder: "+mediaFolder

def getMediaPath(filename):
	global mediaFolder
	file = mediaFolder+filename
	if not os.path.isfile(file):
		print "Note: There is no file at "+file
	return file

def pickAFile(**options):
	global top
	path = tkFileDialog.askopenfilename(parent=top)
	return path

def pickAFolder(**options):
	global mediaFolder
	folder = tkFileDialog.askdirectory()
	if folder == '':
		folder = mediaFolder
	return folder

def pickAColor(**options):
	color = tkColorChooser.askcolor()
	newColor = Color(color[0][0], color[0][1], color[0][2])
	return newColor

#And for those who think of things as folders (5/14/03 AW)
def setMediaFolder():
	global mediaFolder
	file = pickAFolder()
	mediaFolder = file
	print "New media folder: "+mediaFolder

def getMediaFolder(filename):
	global mediaFolder
	file = mediaFolder+filename
	if not os.path.isfile(file) or not os.path.isdir(file):
		print "Note: There is no file at "+file
	return file

def getShortPath(filename):
	dirs = filename.split(os.sep)
	if len(dirs) < 1:	# does split() ever get to this stage?
		return "."
	elif len(dirs) == 1:
		return dirs[0]
	else:
		return (dirs[len(dirs) - 2] + os.sep + dirs[len(dirs) - 1])

def quit():
	sys.exit(0)

##
## COLOR -----------------------------------------------------------------------
##
class Color:
	def __init__(self,r,g,b):
		self.r = int(r) % 256
		self.g = int(g) % 256
		self.b = int(b) % 256

	def __str__(self):
		return "color r="+str(self.getRed())+" g="+str(self.getGreen())+" b="+str(self.getBlue())

	def __repr__(self):
		return "Color("+str(self.getRed())+", "+str(self.getGreen())+", "+str(self.getBlue())+")"

	def __sub__(self,color):
		return Color((self.r-color.r),(self.g-color.g),(self.b-color.b))

	def __add__(self,color):
		return Color((self.r+color.r),(self.g+color.g),(self.b+color.b))

	def __eq__(self,newcolor):
		return ((self.getRed() == newcolor.getRed()) and (self.getGreen() == newcolor.getGreen()) and (self.getBlue() == newcolor.getBlue()))

	def __ne__(self,newcolor):
		return (not self.__eq__(newcolor))

	def distance(self,color):
		r = pow((self.r - color.r),2)
		g = pow((self.g - color.g),2)
		b = pow((self.b - color.b),2)
		return sqrt(r+g+b)

	def difference(self,color):
		return self-color

	def getRGB(self):
		return [self.r, self.g, self.b]

	def setRGB(self,atuple):
		self.r = int(atuple[0]) % 256
		self.g = int(atuple[1]) % 256
		self.b = int(atuple[2]) % 256

	def getRed(self):
		return self.r

	def getGreen(self):
		return self.g

	def getBlue(self):
		return self.b

	def setRed(self,value):
		self.r=int(value) % 256

	def setGreen(self,value):
		self.g=int(value) % 256

	def setBlue(self,value):
		self.b=int(value) % 256

	def makeLighter(self):
		self.r = int((255 - self.r) * .35 + self.r)
		self.g = int((255 - self.g) * .35 + self.g)
		self.b = int((255 - self.b) * .35 + self.b)

	def makeDarker(self):
		self.r = int(self.r	* .65)
		self.g = int(self.g * .65)
		self.b = int(self.b * .65)

##
## Color Constants -------------------------------------------------------------
##
aliceblue = Color(240,248,255)
antiquewhite = Color(250,235,215)
aqua = Color(0,255,255)
aquamarine = Color(127,255,212)
azure = Color(240,255,255)
beige = Color(245,245,220)
bisque = Color(255,228,196)
black = Color(0,0,0)
blanchedalmond = Color(255,235,205)
blue = Color(0,0,255)
blueviolet = Color(138,43,226)
brown = Color(165,42,42)
burlywood = Color(222,184,135)
cadetblue = Color(95,158,160)
chartreuse = Color(127,255,0)
chocolate = Color(210,105,30)
coral = Color(255,127,80)
cornflowerblue = Color(100,149,237)
cornsilk = Color(255,248,220)
crimson = Color(220,20,60)
cyan = Color(0,255,255)
darkblue = Color(0,0,139)
darkcyan = Color(0,139,139)
darkgoldenrod = Color(184,134,11)
darkgray = Color(169,169,169)
darkgreen = Color(0,100,0)
darkkhaki = Color(189,183,107)
darkmagenta = Color(139,0,139)
darkolivegreen = Color(85,107,47)
darkorange = Color(255,140,0)
darkorchid = Color(153,50,204)
darkred = Color(139,0,0)
darksalmon = Color(233,150,122)
darkseagreen = Color(143,188,143)
darkslateblue = Color(72,61,139)
darkslategray = Color(47,79,79)
darkturquoise = Color(0,206,209)
darkviolet = Color(148,0,211)
deeppink = Color(255,20,147)
deepskyblue = Color(0,191,255)
dimgray = Color(105,105,105)
dodgerblue = Color(30,144,255)
firebrick = Color(178,34,34)
floralwhite = Color(255,250,240)
forestgreen = Color(34,139,34)
fuchsia = Color(255,0,255)
gainsboro = Color(220,220,220)
ghostwhite = Color(248,248,255)
gold = Color(255,215,0)
goldenrod = Color(218,165,32)
gray = Color(128,128,128)
green = Color(0,128,0)
greenyellow = Color(173,255,47)
honeydew = Color(240,255,240)
hotpink = Color(255,105,180)
indianred = Color(205,92,92)
indigo = Color(75,0,130)
ivory = Color(255,255,240)
khaki = Color(240,230,140)
lavender = Color(230,230,250)
lavenderblush = Color(255,240,245)
lawngreen = Color(124,252,0)
lemonchiffon = Color(255,250,205)
lightblue = Color(173,216,230)
lightcoral = Color(240,128,128)
lightcyan = Color(224,255,255)
lightgoldenrodyellow = Color(250,250,210)
lightgreen = Color(144,238,144)
lightgrey = Color(211,211,211)
lightpink = Color(255,182,193)
lightsalmon = Color(255,160,122)
lightseagreen = Color(32,178,170)
lightskyblue = Color(135,206,250)
lightslategray = Color(119,136,153)
lightsteelblue = Color(176,196,222)
lightyellow = Color(255,255,224)
lime = Color(0,255,0)
limegreen = Color(50,205,50)
linen = Color(250,240,230)
magenta = Color(255,0,255)
maroon = Color(128,0,0)
mediumaquamarine = Color(102,205,170)
mediumblue = Color(0,0,205)
mediumorchid = Color(186,85,211)
mediumpurple = Color(147,112,219)
mediumseagreen = Color(60,179,113)
mediumslateblue = Color(123,104,238)
mediumspringgreen = Color(0,250,154)
mediumturquoise = Color(72,209,204)
mediumvioletred = Color(199,21,133)
midnightblue = Color(25,25,112)
mintcream = Color(245,255,250)
mistyrose = Color(255,228,225)
moccasin = Color(255,228,181)
navajowhite = Color(255,222,173)
navy = Color(0,0,128)
oldlace = Color(253,245,230)
olive = Color(128,128,0)
olivedrab = Color(107,142,35)
orange = Color(255,165,0)
orangered = Color(255,69,0)
orchid = Color(218,112,214)
palegoldenrod = Color(238,232,170)
palegreen = Color(152,251,152)
paleturquoise = Color(175,238,238)
palevioletred = Color(219,112,147)
papayawhip = Color(255,239,213)
peachpuff = Color(255,218,185)
peru = Color(205,133,63)
pink = Color(255,192,203)
plum = Color(221,160,221)
powderblue = Color(176,224,230)
purple = Color(128,0,128)
red = Color(255,0,0)
rosybrown = Color(188,143,143)
royalblue = Color(65,105,225)
saddlebrown = Color(139,69,19)
salmon = Color(250,128,114)
sandybrown = Color(244,164,96)
seagreen = Color(46,139,87)
seashell = Color(255,245,238)
sienna = Color(160,82,45)
silver = Color(192,192,192)
skyblue = Color(135,206,235)
slateblue = Color(106,90,205)
slategray = Color(112,128,144)
snow = Color(255,250,250)
springgreen = Color(0,255,127)
steelblue = Color(70,130,180)
tan = Color(210,180,140)
teal = Color(0,128,128)
thistle = Color(216,191,216)
tomato = Color(255,99,71)
turquoise = Color(64,224,208)
violet = Color(238,130,238)
wheat = Color(245,222,179)
white = Color(255,255,255)
whitesmoke = Color(245,245,245)
yellow = Color(255,255,0)
yellowgreen = Color(154,205,50)

##
## PICTURE FRAME ---------------------------------------------------------------
##
class PictureFrame(Toplevel):

	def __init__(self, picture):
		Toplevel.__init__(self)
		self.title(picture.title)
		self.pic = picture

	def destroy(self):
		self.pic.windowInactive()
		Toplevel.destroy(self)

##
## PICTURE ---------------------------------------------------------------------
##
class Picture:

	def __init__(self, auto_repaint = False):
		self.title = "Unnamed"
		self.dispImage = None
		self.winActive = 0
		self.__autoRepaint = auto_repaint
		self.__visibleFrame = False
		self.__eventBindings = {}
		# bind the mouse event to show the pixel information
		#	self.addEventHandler("<Button-1>", self.doPickColor)
		#	self.addEventHandler("<B1-Motion>", self.doPickColor)

	def __initializePicture(self, surface, filename, title):
		self.surf = surface
		# we get the pixels array from the surface
		self.pixels = pygame.surfarray.pixels3d(self.surf)
		self.filename = filename
		self.title = title
		self.__update()

	def setAutoRepaint(self, boolean):
		self.__autoRepaint = boolean
		self.__update()

	def windowInactive(self):
		del self.dispImage, self.item, self.canvas
		self.winActive = 0
		self.__visibleFrame = False

	def createImage(self, width, height):
		# fail if dimensions are invalid
		if (width < 0 or height < 0):
			raise ValueError("createImage(" + str(width) + ", " + str(height) + "): Invalid image dimensions")
		else:
			self.__initializePicture(pygame.Surface((width, height)), '', 'None')

	def loadImage(self,filename):
		global mediaFolder
		if not os.path.isabs(filename):
			filename = mediaFolder + filename
		# fail if file does not exist
		if not os.path.isfile(filename):
		 	raise ValueError(("loadImage(" + filename + "): No such file"))
		else:
			from Image import open
			mode = "RGB"
			image = open(filename).convert(mode)
			size = image.size
			data = image.tostring()
			# initialize this picture with new properties
			self.__initializePicture(pygame.image.fromstring(data, size, mode), filename, getShortPath(filename))

	def copyFromImage(self, picture, x=1, y=1, width=None, height=None):
	# copies and image from another picture, replacing this one
		# note that the coordinates are one based
		# copy the other picture's image
		image = picture.getImage().copy()
	# crop to the dimensions specified
		imageWidth = picture.getWidth()
		imageHeight = picture.getHeight()
		# throw exceptions if the values are invalid
		if (x < 1 or y < 1 or x >= imageWidth or y >= imageHeight):
			raise ValueError(('Invalid x/y coordinates specified'))
		# width || height < 1 implies a full image copied (maybe with warning)
		if (width == None and height == None):
			width = imageWidth
			height = imageHeight
		# fail if either is None, or they are < 1
		elif (width == None or height == None or width < 1 or height < 1):
			raise ValueError(('Invalid width/height specified'))
		# get/bound the actual image coordinates
		x1 = x-1
		y1 = y-1
		x2 = x1+min(width, imageWidth-x1)
		y2 = y1 + min(height, imageHeight-y1)
		# get the sub image with the dimensions specified [x1,y1,x2,y1)
		box = (x1, y1, x2, y2)
		image = image.crop(box)
		# get the image properties
		mode = image.mode
		size = image.size
		data = image.tostring()
		# initialize this picture with new properties
		self.__initializePicture(pygame.image.fromstring(data, size, mode), picture.filename, picture.title)

	def overlayImage(self, picture, x=0, y=0):
		if x == 0:
			# center x
			x = (self.getWidth()/2)-(picture.getWidth()/2)+1
		if y == 0:
			# center y
			y = (self.getHeight()/2)-(picture.getHeight()/2)+1
		# blit the other image
		# note that we must unlock both image surfaces
		self.surf.unlock()
		picture.surf.unlock()
		self.surf.blit(picture.surf, (x-1, y-1))
		picture.surf.lock()
		self.surf.lock()
		self.__update()

	def clear(self, color=black):
		# clears the picture pixels to black
		self.setPixels(color)

	def __str__(self):
		return "Picture, filename "+self.filename+" height "+str(self.getHeight())+" width "+str(self.getWidth())

	def __update(self):
		if self.__visibleFrame and self.__autoRepaint:
			self.repaint()

	def repaint(self):
		if self.winActive:
			self.canvas.delete(self.item)
			self.dispImage = ImageTk.PhotoImage(self.getImage())
			self.item = self.canvas.create_image(0, 0, image=self.dispImage, anchor='nw')
			self.canvas.pack()
			self.canvas.update()
			self.frame.title(self.title)
		else:
			self.show()

	def show(self):
		if not self.winActive:
			self.frame = PictureFrame(self)
			self.canvas = Canvas(self.frame, width=self.getWidth(),
				height=self.getHeight(), highlightthickness=0)

			self.dispImage = ImageTk.PhotoImage(self.getImage())
			self.item = self.canvas.create_image(0, 0, image=self.dispImage, anchor='nw')
			self.canvas.pack()
			self.winActive = 1
			self.__visibleFrame = True
			# bind all events
			for eventStr, callback in self.__eventBindings.items():
				self.canvas.bind(eventStr, callback)
		else:
			self.repaint()

	def doPickColor(self, event):
		x = event.x+1
		y = event.y+1
		if (0 < x and x <= self.getWidth() and 0 < y and y < self.getHeight()):
			pixel = self.getPixel(x, y)
			print pixel;

	def hide(self):
		if self.winActive:
			self.frame.destroy()

	def setTitle(self, title):
		self.title = title
		self.__update()

	def getTitle(self):
		return self.title

	def getImage(self):
		# seems to return a PIL image of the same dimensions
		data = pygame.image.tostring(self.surf, "RGB", 0)
		image = fromstring("RGB", (self.getWidth(), self.getHeight()), data)
		return image

	def getWidth(self):
		return self.surf.get_width()

	def getHeight(self):
		return self.surf.get_height()

	def getPixel(self,x,y):
		return Pixel(self.pixels,x,y)

	def getPixels(self):
		collect = []
		# we want the width and the height inclusive since Pixel() is one based
		# we increase the ranges so that we don't have to add in each iteration
		for x in range(1,self.getWidth()+1):
			for y in range(1,self.getHeight()+1):
				collect.append(Pixel(self.pixels,x,y))
		return collect

	def setPixels(self, color):
		# set all the pixels in this picture to a given color
		try:
			self.surf.fill(color.getRGB())
			self.__update()
		except:
			raise AttributeError('setPixels(color): Picture has not yet been initialized.')
	def writeTo(self,filename):
		if not os.path.isabs(filename):
			filename = mediaFolder + filename
		#pygame.image.save(self.surf, filename)
		image = self.getImage()
		image.save(filename, None)

	# TODO: add bounds checks for all the following functions to ensure that they are one based
	# draw stuff on pictures
	def addRectFilled(self,acolor,x,y,w,h):
		pygame.draw.rect(self.surf, acolor.getRGB(), pygame.Rect(x-1, y-1, w, h))
		self.__update()

	def addRect(self, acolor,x,y,w,h, width=1):
		pygame.draw.rect(self.surf, acolor.getRGB(), pygame.Rect(x-1, y-1, w, h), width)
		self.__update()

	# Draws a polygon on the image.
	def addPolygon(self,acolor,pointList):
		pygame.draw.polygon(self.surf, acolor.getRGB(), pointList, 1)
		self.__update()

	def addPolygonFilled(self, acolor,pointList):
		pygame.draw.polygon(self.surf, acolor.getRGB(), pointList, 0)
		self.__update()

	def addOvalFilled(self, acolor,x,y,w,h):
		pygame.draw.ellipse(self.surf, acolor.getRGB(), pygame.Rect(x-1, y-1, w, h))
		self.__update()

	def addOval(self, acolor,x,y,w,h):
		pygame.draw.ellipse(self.surf, acolor.getRGB(), pygame.Rect(x-1, y-1, w, h), 1)
		self.__update()

	def addArcFilled(self, acolor,x,y,w,h,start,angle):
		#this is an estimation def needs to be done another way but I need to figure out how
		if w > h:
			pygame.draw.arc(self.surf, acolor.getRGB(), Rect(x, y, w, h), start, angle, h/2)
		else:
			pygame.draw.arc(self.surf, acolor.getRGB(), Rect(x, y, w, h), start, angle, w/2)
		self.__update()


	def addArc(self, acolor,x,y,w,h,start,angle):
		pygame.draw.arc(self.surf, acolor.getRGB(), Rect(x, y, w, h), start, angle)
		self.__update()

	def addLine(self, acolor, x1, y1, x2, y2, width=1):
		pygame.draw.line(self.surf, acolor.getRGB(), [x1-1, y1-1], [x2-1, y2-1], width)
		self.__update()

	def addText(self, acolor, x, y, string):
		global defaultFont
		self.addTextWithStyle(acolor, x, y, string, defaultFont)
		self.__update()

	def addTextWithStyle(self, acolor, x, y, string, font):
		# add the text with the specified font
		textSurf = font.render(string, True, acolor.getRGB())
		self.surf.unlock()
		self.surf.blit(textSurf, (x-1, y-1))
		self.surf.lock()
		self.__update()

	def addEventHandler(self, tkEventStr, callback):
		# see: http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
		# for more information
		self.__eventBindings[tkEventStr] = callback
		if self.winActive:
			self.canvas.bind(tkEventStr, callback)

	def removeEventHandler(self, tkEventStr):
		if tkEventStr in self.__eventBindings:
			del self.__eventBindings[tkEventStr]
			if self.winActive:
				self.canvas.unbind(tkEventStr)

	def removeAllEventHandlers(self):
		if self.winActive:
			for eventStr, callback in self.__eventBindings.items():
					self.canvas.unbind(eventStr)
		self.__eventBindings.clear()

#
# PIXEL ------------------------------------------------------------------------
#
class Pixel:

	def __init__(self,picture,x,y):
		lenX = len(picture)
		lenY = len(picture[0])
		if lenX > 0 and lenY > 0:
			self.x = (x - 1) % lenX
			self.y = (y - 1) % lenY
			# we still want to fail if the accessible indices are out of wrap-around bounds so we
			# can not use self.x, and self.y below
			self.pix = picture[x-1][y-1]
		else:
			raise ValueError(('Invalid image dimensions (' + str(lenX) + ', ' + str(lenY) + ')'))
	def __str__(self):
		return "Pixel, color="+str(self.getColor())

	def setRed(self,r):
		if 0 <= r and r <= 255:
			self.pix[0] = r
		else:
			raise ValueError(('Invalid red component value (' + str(r) + '), expected value within [0, 255]'))
	def setGreen(self,g):
		if 0 <= g and g <= 255:
			self.pix[1] = g
		else:
			raise ValueError(('Invalid green component value (' + str(g) + '), expected value within [0, 255]'))
	def setBlue(self,b):
		if 0 <= b and b <= 255:
			self.pix[2] = b
		else:
			raise ValueError(('Invalid blue component value (' + str(b) + '), expected value within [0, 255]'))
	def getRed(self):
		return int(self.pix[0])

	def getGreen(self):
		return int(self.pix[1])

	def getBlue(self):
		return int(self.pix[2])

	def getColor(self):
		return Color(self.getRed(),self.getGreen(), self.getBlue())

	def setColor(self,color):
		self.setRed(color.getRed())
		self.setGreen(color.getGreen())
		self.setBlue(color.getBlue())

	def getX(self):
		return self.x + 1

	def getY(self):
		return self.y + 1

##
## MOVIE FRAME ---------------------------------------------------------------
##
class MovieFrame(Toplevel):

	def __init__(self, movie):
		Toplevel.__init__(self)
		self.title("Frame 0")
		self.movie = movie

	def destroy(self):
		self.movie.windowInactive()
		Toplevel.destroy(self)

##
## MOVIE -----------------------------------------------------------------------
##
class Movie:

	def __init__(self, baseName="frame", format="jpg"):
		self.frames = []
		self.baseFileName = baseName
		self.fileFormat = format
		self.fps = 1
		self.curFrame = 0
		self.winActive = 0
		self.playing = False

	def __len__(self):
		return len(self.frames)

	def __getitem__(self,item):
		# returns the i'th frame of the movie
		return self.frames[item]

	def __padNumberString(self, expectedNumDigits, number):
		if number <= 0:
			# return all zeros
			return "0"*expectedNumDigits
		else:
			# returns n zeroes followed by the number
			numDigits = int(math.log10(number))+1
			return "0"*(expectedNumDigits-numDigits) + str(number)

	def __str__(self):
		return "Movie with %d frames." % str(len(self))

	def windowInactive(self):
		# TODO: remove stuff
		self.winActive = 0

	def addFrameFromPicture(self, picture):
		self.frames.append(picture)

	def addFrame(self, path):
		# create a new picture and load from the path
		p = Picture()
		p.loadImage(path)
		self.addFrameFromPicture(p)

	def clear(self):
		for idx in range(len(self.frames)):
			del self.frames[idx]

	def setFPS(self, fps):
		self.fps = fps

	def getFPS(self):
		return self.fps

	def loadFramesFromDirectory(self, directory, baseName):
		# ensure that the directory exists
		if not os.path.isdir(directory):
			raise ValueError("Provided directory (%s) does not exist." % directory)
		directory = os.path.abspath(directory)	# make it an abs path
		# ensure that the directory contains files of the specified base name
		hasMovieFrames = False
		expectedFilesPattern = re.compile("%s\d+\.?(\w*)" % (baseName), re.IGNORECASE)
		fileList = os.listdir(directory)
		for file in fileList:
			match = expectedFilesPattern.match(file)
			if match:
				# add the frame to the current movie
				hasMovieFrames = True
				# save the file format since we are here
				self.fileFormat = match.group(1)
				break
		# now check if we did not encounter frame files
		if not hasMovieFrames:
			raise ValueError("Provided directory (%s) does not contain movie frames." % directory)
		# clear the current frames in the movie first
		self.clear()
		# now, for each file in the directory with the base file name, read
		for file in fileList:
			if expectedFilesPattern.match(file):
				# add the frame to the current movie
				path = os.path.join(directory, file)
				self.addFrame(path)
		# and store the movie file format, and base file name
		self.baseFileName = baseName

	def writeFramesToDirectory(self, directory):
		# return if there are no frames in the movie
		if len(self.frames) == 0:
			raise ValueError("There are no frames in this movie.")
		# ensure we have a valid base filename, since we will be removing files
		# based on it
		validBaseNamePattern = re.compile("[\w.]+")
		if not validBaseNamePattern.match(self.baseFileName):
			raise ValueError("Invalid base filename (%s)" % self.baseFileName)
		# fail if the provided path is not a directory
		if not os.path.isdir(directory):
			raise ValueError("Provided directory (%s) does not exist." % directory)
		# otherwise, for each file in this directory, remove all that match the
		# current frame name
		existingFilesPattern = re.compile("%s\d+\.%s" % (self.baseFileName, self.fileFormat), re.IGNORECASE)
		directory = os.path.abspath(directory)	# make it an abs path
		fileList = os.listdir(directory)
		for file in fileList:
			if existingFilesPattern.match(file):
				# remove it so we can start fresh
				os.remove(os.path.join(directory, file))
		# after we have removed all files with the expected name, we can simply
		# write each frame according to it's index
		numFrames = len(self.frames)
		numPadding = int(math.log10(numFrames))+1
		absBasePath = os.path.join(directory, self.baseFileName)
		for idx in range(numFrames):
			# generate the expected filename
			filename = "%s%s.%s" % (absBasePath,
									self.__padNumberString(numPadding, idx),
									self.fileFormat)
			# and write each picture
			self.frames[idx].writeTo(filename)
		# let the user know we saved
		print "Movie saved."

	def update(self):
		frame = self.frames[self.curFrame]
		if not self.winActive:
			self.frame = MovieFrame(self)
			self.canvas = Canvas(self.frame,
							width=frame.getWidth(),
							height=frame.getHeight(),
							highlightthickness=0)
			self.dispImage = ImageTk.PhotoImage(frame.getImage())
			self.item = self.canvas.create_image(0, 0, image=self.dispImage, anchor='nw')
			self.winActive = 1
		else:
			self.canvas.delete(self.item)
			self.dispImage = ImageTk.PhotoImage(frame.getImage())
			self.item = self.canvas.create_image(0, 0, image=self.dispImage, anchor='nw')
		# update he canvas
		self.canvas.pack()
		self.canvas.update()

	def nextFrame(self):
		# if this is the last frame, then return
		if self.curFrame == len(self.frames):
			self.stop()
			return;
		# update the movie frame
		self.update()
		# set the cur frame title
		self.frame.title("Frame: %d" % self.curFrame)
		# move onto the next frame
		self.curFrame = self.curFrame + 1
		# reset the timer
		delay = 1000/self.fps
		pygame.time.wait(delay)
		self.nextFrame()
		# self.timer = Timer(delay, self.nextFrame)
		# self.timer.start()

	def play(self):
		# return if there are no frames to play
		if len(self.frames) == 0:
			return
		# if we are at the end, and the user wants to play again, then rewind
		if self.curFrame == len(self.frames):
			self.rewind()
		# and start playing
		self.playing = True
		self.nextFrame()

	def stop(self):
		self.playing = False

	def rewind(self):
		self.curFrame = 0
		# update the movie frame
		self.update()


##
## Global picture functions ----------------------------------------------------
##
def makePicture(filename):
	picture = Picture()
	picture.loadImage(filename)
	try:
		w = picture.getWidth()
		return picture
	except:
		print "Was unable to load the image in " + filename +"\nMake sure it's a valid image file."

def makeEmptyPicture(width, height):
	picture = Picture()
	picture.createImage(width, height)
	return picture

def duplicatePicture(picture):
	if not picture.__class__ == Picture:
		raise ValueError("duplicatePicture(picture): First input is not a picture")
	newPicture = Picture()
	newPicture.copyFromImage(picture)
	return newPicture

def makeStyle(fontname, fontsize=10, bold=False, italic=False):
	# try to make a font style with the given parameters
	global defaultFont
	try:
		return pygame.font.SysFont(fontname, fontsize, bold, italic)
	except:
		print "makeStyle(fontname,fontsize,bold,italic): No such font found"
		return defaultFont
def setPixels(picture,color):
	if not picture.__class__ == Picture:
		raise ValueError("setPixels(picture,color): First input is not a picture")
	if not color.__class__ == Color:
		raise ValueError("setPixels(picture,color): Second input is not a color.")
	return picture.setPixels(color)

def getPixel(picture,x,y):
	if not picture.__class__ == Picture:
		raise ValueError("getPixel(picture,x,y): Input is not a picture")
	return picture.getPixel(x,y)

def getPixels(picture):
	if not picture.__class__ == Picture:
		raise ValueError("getPixels(picture): Input is not a picture")
	return picture.getPixels()

def getWidth(picture):
	if not picture.__class__ == Picture:
		raise ValueError("getWidth(picture): Input is not a picture")
	return picture.getWidth()

def getHeight(picture):
	if not picture.__class__ == Picture:
		raise ValueError("getHeight(picture): Input is not a picture")
	return picture.getHeight()

def show(picture, title=None):
	if not picture.__class__ == Picture:
		raise ValueError("show(picture): Input is not a picture")
	picture.show()

def repaint(picture):
	if not picture.__class__ == Picture:
		raise ValueError("repaint(picture): Input is not a picture")
	picture.repaint()

def addLine(picture,x1,y1,x2,y2):
	if not picture.__class__ == Picture:
		raise ValueError("addLine(picture,x1,y1,x2,y2): Input is not a picture")
	picture.addLine(black,x1,y1,x2,y2)

def addText(picture,x1,y1,string):
	if not picture.__class__ == Picture:
		raise ValueError("addText(picture,x1,y1,string): Input is not a picture")
	picture.addText(black,x1,y1,string)

def addRect(picture,x,y,w,h):
	if not picture.__class__ == Picture:
		raise ValueError("addRect(picture,x,y,w,h): Input is not a picture")
	picture.addRect(black,x,y,w,h)

def addRectFilled(picture,x,y,w,h,acolor):
	if not picture.__class__ == Picture:
		raise ValueError("addRectFilled(picture,x,y,w,h,acolor): Input is not a picture")
	picture.addRectFilled(acolor,x,y,w,h)

def addPolygon(picture,pointList,acolor):
	if not picture.__class__ == Picture:
		raise ValueError("addPolygon(picture,pointList,acolor): Input is not a picture")
	picture.addPolygon(acolor, pointList)

def addPolygonFilled(picture,pointlist,acolor):
	if not picture.__class__ == Picture:
		raise ValueError("addPolygonFilled(picture,pointlist,acolor): Input is not a picture")
	picture.addPolygonFilled(acolor, pointlist)

def writePictureTo(pict,filename):
	if not pict.__class__ == Picture:
		raise ValueError("writePictureTo(pict,filename): Input is not a picture")
	pict.writeTo(filename)
	#if not os.path.exists(filename):
	#	print "writePictureTo(pict,filename): Path is not valid"
	#	raise ValueError

##
## Global pixel functions ------------------------------------------------------
##
def setRed(pixel,value):
	if not pixel.__class__ == Pixel:
		raise ValueError("setRed(pixel,value): Input is not a pixel")
	pixel.setRed(value)

def getRed(pixel):
	if not pixel.__class__ == Pixel:
		raise ValueError("getRed(pixel): Input is not a pixel")
	return pixel.getRed()

def setBlue(pixel,value):
	if not pixel.__class__ == Pixel:
		raise ValueError("setBlue(pixel,value): Input is not a pixel")
	pixel.setBlue(value)

def getBlue(pixel):
	if not pixel.__class__ == Pixel:
		raise ValueError("getBlue(pixel): Input is not a pixel")
	return pixel.getBlue()

def setGreen(pixel,value):
	if not pixel.__class__ == Pixel:
		raise ValueError("setGreen(pixel,value): Input is not a pixel")
	pixel.setGreen(value)

def getGreen(pixel):
	if not pixel.__class__ == Pixel:
		raise ValueError("getGreen(pixel): Input is not a pixel")
	return pixel.getGreen()

def getColor(pixel):
	if not pixel.__class__ == Pixel:
		raise ValueError("getColor(pixel): Inputis not a pixel")
	return pixel.getColor()

def setColor(pixel,color):
	if not pixel.__class__ == Pixel:
		raise ValueError("setColor(pixel,color): Input is not a pixel.")
	if not color.__class__ == Color:
		raise ValueError("setColor(pixel,color): Input is not a color.")
	pixel.setColor(color)

def getX(pixel):
	if not pixel.__class__ == Pixel:
		raise ValueError("getX(pixel): Input is not a pixel")
	return pixel.getX()

def getY(pixel):
	if not pixel.__class__ == Pixel:
		raise ValueError("getY(pixel): Input is not a pixel")
	return pixel.getY()

##
## Global color functions ------------------------------------------------------
##
def distance(c1,c2):
	if not c1.__class__ == Color:
		raise ValueError("distance(c1,c2): First input is not a color.")
	if not c2.__class__ == Color:
		raise ValueError("distance(c1,c2): Second input is not a color.")
	return c1.distance(c2)

def makeDarker(color):
	if not color.__class__ == Color:
		raise ValueError("makeDarker(color): Input is not a color.")
	color.makeDarker()
	return color

def makeLighter(color):
	if not color.__class__ == Color:
		raise ValueError("makeLighter(color): Input is not a color.")
	color.makeLighter()
	return color

def makeColor(red,green,blue):
	return newColor(red,green,blue)

def newColor(red,green,blue):
	return Color(red,green,blue)

##
## Global movie functions ------------------------------------------------------
##
def makeMovie():
    return Movie()

def makeMovieFromInitialFile(filename):
    movie = Movie()
    # get the basename and directory from the file
    (dir, file) = os.path.split(filename)
    baseFilePattern = re.compile("([a-zA-Z_-]+)\d+\.?\w*", re.IGNORECASE)
    match = baseFilePattern.match(file)
    if match:
    	# get the base filename
    	file = match.group(1)
	# load from the directory and basename
	movie.loadFramesFromDirectory(dir+os.sep, file)
    # return the movie
    return movie

def addFrameToMovie(a, b):
    frame = None
    movie = None
    if a.__class__ == Movie:
        movie = a
        frame = b
    else:
        movie = b
        frame = a
    # ensure that one is the movie and the other the path
    if movie.__class__ != Movie or frame.__class__ != String:
        raise ValueError("addFrameToMovie(frame, movie): frame is not a string or movie is not a Movie object.")
	# add the frame
    movie.addFrame(frame)


def writeFramesToDirectory(movie, directory=None):
    if movie.__class__ != Movie:
        raise ValueError("writeFramesToDirectory(movie, directory): movie is not a Movie object.")
	# save to media folder if none specified
    if directory == None:
        directory = mediaFolder
    # write the movie to the directory
    movie.writeFramesToDirectory(directory)

def playMovie(movie):
    if movie.__class__ != Movie:
        raise ValueError("playMovie(movie): movie is not a Movie object.")
	# play the movie
    movie.play()



##
## The Sound Stuff
##

##
## SOUND -----------------------------------------------------------------------
##

### The entire Sound and Sample class is deprecated.
### Sound functionality is now done by the tkSnack library

### TO be compatible with the book and older versions, make a a wrapper
### Sound class.
class Sound:
	def __init__(self,filename=None):
		global mediaFolder
		global defaultFrequency
		global defaultSampleSize
#		try:
#			self.m = pygame.mixer
#			#self.m.init(22050, -16, False)
#			#self.tkSound = tkSnack.Sound();
#		except:
#			raise StandardError(("Unable to initialize sound system."))

		if (filename == None):
			self.tkSound = tkSnack.Sound();
			self.tkSound.configure(frequency=defaultFrequency)
			self.tkSound.length(defaultSampleSize, unit="SECONDS")
#			self.s = pygame.sndarray.make_sound( Numeric.array([0]) )
		else:
			if not os.path.isabs(filename):
				filename = mediaFolder + filename
			if not os.path.isfile(filename):
				raise ValueError(("There is no file at "+filename))
			self.tkSound = tkSnack.Sound(load=filename)

#			if not os.path.isabs(filename):
#				filename = mediaFolder + filename
#			self.filename = filename
#			try:
#				self.s = self.m.Sound(filename)
#			except:
#				raise IOError(('Unable to open file (' + filename + ')'))
#			self.a = pygame.sndarray.samples(self.s)


	def __str__(self):
		return "Sound of length "+str(self.getLength())

	def __rep__(self):
		return "Sound of length "+str(self.getLength())

		def __class__(self):
				return Sound

	def makeEmptyLength(self,sec):
		global defaultFrequency
		if sec < 0:
			raise ValueError("Sound.makeEmptyLength: Length given is negative")		
		length = self.getSamplingRate()*sec
		self.tkSound.length(int(length))
		#self.s = pygame.sndarray.make_sound( Numeric.zeros( sec * defaultFrequency ) )
		#self.a = pygame.sndarray.samples(self.s)

	def play(self):
		try:
			self.tkSound.play();
		except:
			print "Trouble accessing the sound device."

	def playInRange(self,start,stop):
		if ( start < 1 ):
			raise ValueError("Starting position cannot be smaller than 1.")
		if ( stop <= start ):
			raise ValueError("Ending position cannot be smaller or equal to start.")
		if ( stop > self.getLength() ):
			raise ValueError("Ending position is great than the sound length.")
		self.tkSound.play(start=s,end=e)
#		try:
#			if start > 0 and stop <= self.getLength() and start < stop:
#				tmpsnd = pygame.sndarray.make_sound( self.a[start-1:stop-1] )
#				tmpsnd.play()
#			else:
#				raise ValueError(('Invalid range (' + str(start) + ', ' + str(stop) + ') in PlayInRange().'))
#		except ValueError:
#			# pass on the value error
#			raise
#		except:
#			exc_type, ex_value, exc_tb = sys.exc_info()
#			print exc_type
#			print exc_value
#			print traceback.extract_tb(exc_tb)
#			print "Trouble accessing the sound device."

	def blockingPlay(self):
		self.tkSound.play(blocking=1)
#		
#		try:
#			chan = self.s.play()
#			while chan.get_busy(): #still playing
#				pygame.time.wait(10)
#		except:
#			print "Trouble accessing the sound device."


	def blockingPlayInRange(self,start,stop):
		if ( start < 1 ):
			raise ValueError("Starting position cannot be smaller than 1.")
		if ( stop <= start ):
			raise ValueError("Ending position cannot be smaller or equal to start.")
		if ( stop > self.getLength() ):
			raise ValueError("Ending position is great than the sound length.")
				
		self.tkSound.play(blocking=1,start=s, end=e)
#		try:
#			if start > 0 and stop <= self.getLength() and start < stop:
#				tmpsnd = pygame.sndarray.make_sound( self.a[start-1:stop-1] )
#				chan = tmpsnd.play()
#				while chan.get_busy(): #still playing
#					time.wait(10)
#			else:
#				raise ValueError(('Invalid range (' + str(start) + ', ' + str(stop) + ') in blockingPlayInRange().'))
#		except ValueError:
#			# pass on the value error
#			raise
#		except:
#			exc_type, ex_value, exc_tb = sys.exc_info()
#			print exc_type
#			print exc_value
#			print traceback.extract_tb(exc_tb)
#			print "Trouble accessing the sound device."

	def getSamples(self):
		return Samples(self)

	def getLength(self):
		return self.tkSound.length()

	def getSampleValue(self,index):
		if ( index-1 < 0 ):
			raise ValueError("Sound.getSampleValue: index is smaller than 1")
		if ( index > self.getLength() ):
			raise ValueError("Sound.getSampleValue: index is greater than sound length")
		return self.tkSound.sample(index-1)
 
	def setSampleValue(self,index,value):
		if not type(value) == int:
			raise ValueError("Sound.setSampleValue: Sample value must be int")
		if ( index-1 < 0 ):
			raise ValueError("Sound.setSampleValue: index is smaller than 1")
		if ( index > self.getLength() ):
			raise ValueError("Sound.setSampleValue: index is greater than sound length")		
		self.tkSound.sample(index-1, value)

	def getSamplingRate(self):
		return self.tkSound["frequency"]

	def getSampleObjectAt(self,index):
		if index > 0 and index <= self.getLength():
			return Sample(self,index)
		else:
			raise ValueError(("invalid index in getSampleObjectAt()."))

	def writeTo(self,filename):
		global mediaFolder
		if not os.path.isabs(filename):
			filename = mediaFolder + filename
		self.tkSound.write(filename)
		

class Samples:
	def __init__(self,aSound):
		self.myList = []
		self.sound = aSound
		for s in range(1,aSound.getLength()+1):
			self.myList.append(Sample(aSound,s))

	def __str__(self):
		return "Samples, length "+str(self.sound.getLength())

	def __rep__(self):
		return "Samples, length "+str(self.sound.getLength())

	def __getitem__(self,item):
		return self.myList[item]

	def __setitem__(self,item,value):
		self.sound.setSampleValue(item,value)

	def getSound(self):
		return self.sound


class Sample:
	def __init__(self,aSound,index):
		self.sound=aSound
		self.index=index

	def __str__(self):
		return "Sample at "+str(self.index)+" value at "+str(self.getValue())

	def __rep__(self):
		return "Sample at "+str(self.index)+" value at "+str(self.getValue())

	def setValue(self,value):
		self.sound.setSampleValue(self.index,int(round(value)))

	def getValue(self):
		return self.sound.getSampleValue(self.index)

	def getSound(self):
		return self.sound

##
## Global sound functions ------------------------------------------------------
##
def makeSound(filename):	
	global mediaFolder
	if not os.path.isabs(filename):
		filename = mediaFolder + filename
	if not os.path.isfile(filename):
		raise ValueError(("There is no file at "+filename))
	sound = Sound(filename)
	return sound

def makeEmptySound(length):
	snd = Sound()
	snd.makeEmptyLength(length)
	#snd.makeEmptyLength(size)
	return snd


def getSamples(sound):
	if not sound.__class__ == Sound:
		raise ValueError("getSamples(sound): Input is not a sound.")
	return Samples(sound)

def play(sound):
	if not sound.__class__ == Sound:
		raise ValueError("play(sound): Input is not a sound.")
	sound.play()

def blockingPlay(sound):
	if not sound.__class__ == Sound:
		raise ValueError("blockingPlay(sound): Input is not a sound.")
	sound.blockingPlay()


#20June03 new functionality in JavaSound (ellie)
def playInRange(sound,s,e):
		print sound.__class__
		if not sound.__class__ == Sound:
			raise ValueError("playInRange(sound,start,stop):  Input is not a sound.")
		sound.playInRange(s, e)

#20June03 new functionality in JavaSound (ellie)
def blockingPlayInRange(sound,s,t):
		if not sound.__class__ == Sound:
			raise ValueError("blockingPlayInRange(sound,start,stop): Input is not a sound.")
		sound.blockingPlayInRange(s, t)

def getSamplingRate(sound):
	if not sound.__class__ == Sound:
		raise ValueError("getSamplingRate(sound): Input is not a sound.")
	return sound.getSampleRate()

def setSampleValueAt(sound,index,value):
	if not sound.__class__ == Sound:
		raise ValueError("setSampleValueAt(sound,index,value): Input is not a sound.")
	sound.setSampleValue(index,value)

def getSampleValueAt(sound,index):
	if not sound.__class__ == Sound:
		raise ValueError("getSampleValueAt(sound,index): Input is not a sound.")
	return sound.getSampleValue(index)

def getSampleObjectAt(sound,index):
	if not sound.__class__ == Sound:
		raise ValueError("getSampleObjectAt(sound,index): Input is not a sound.")
	return sound.getSampleObjectAt(index)

def getLength(sound):
	if not sound.__class__ == Sound:
		raise ValueError("getLength(sound): Input is not a sound.")
	return sound.getLength()

def writeSoundTo(sound,filename):
	if not sound.__class__ == Sound:
		raise ValueError("writeSoundTo(sound,filename): Input is not a sound.")
	sound.writeTo(filename)

def setSample(sample,value):
	if not sample.__class__ == Sample:
		raise ValueError("setSample(sample,value): Input is not a sample.")
	# Need to coerce value to integer
	return sample.setValue(value)

def getSample(sample):
	if not sample.__class__ == Sample:
		raise ValueError("getSample(sample): Input is not a sample.")
	return sample.getValue()

def getSound(sample):
	if not sample.__class__ == Sample:
		raise ValueError("getSound(sample): Input is not a sample.")
	return sample.getSound()


# This function plots the sound graph.
# By default the size of the graph is 1024x300
# TODO: Make it zoom capable
def plotWaveform(snd, width=1024, height=300):
	if not snd.__class__ == Sound:
		raise ValueError("plotSound(sound): The parameter is not sound.")
	win = Toplevel()

	c = tkSnack.SnackCanvas(win, background="#060", width=width, height=height)
	c.pack()
	c.create_waveform(0, 0, fill="#0f0" ,sound=snd.tkSound, width=width, height=height, zerolevel=1)
	

def plotSpectrogram(snd, width=1024, height=300):
	if not snd.__class__ == Sound:
		raise ValueError("plotSound(sound): The parameter is not sound.")
	win = Toplevel()

	c = tkSnack.SnackCanvas(win, background="#060", width=width, height=height)
	c.pack()
	c.create_spectrogram(0, 0, sound=snd.tkSound, width=width, height=height)

def plotSpectrum(snd, width=1024, height=300):
	if not snd.__class__ == Sound:
		raise ValueError("plotSound(sound): The parameter is not sound.")
	win = Toplevel()

	c = tkSnack.SnackCanvas(win, background="#060",width=width, height=height)
	c.pack()
	c.create_section(0, 0, fill="#0f0", sound=snd.tkSound, width=width, height=height)
	#c.create_spectrogram(0, 150, sound=snd, height=200)

##
## Global turtle functions -----------------------------------------------------
##
from turtle import *
def turn(turtle, degrees=90):
    if not turtle.__class__ == Turtle:
        raise ValueError("turn(turtle, degrees): Input is not a turtle")
    else:
        turtle.turn(degrees)

def turnRight(turtle):
    if not turtle.__class__ == Turtle:
        raise ValueError("turnRight(turtle, degrees): Input is not a turtle")
    else:
        turtle.turnRight()

def turnToFace(turtle, turtle2):
    if not (turtle.__class__ == Turtle and turtle2.__class__ == Turtle):
        raise ValueError("turnToFace(turtle, x, y): Input is not a turtle")
    else:
        turtle.turnToFace(turtle2)

def turnLeft(turtle):
    if not turtle.__class__ == Turtle:
        raise ValueError("turnLeft(turtle, degrees): Input is not a turtle")
    else:
        turtle.turnLeft()

def forward(turtle, pixels=100):
    if not turtle.__class__ == Turtle:
        raise ValueError("forward(turtle, pixels): Input is not a turtle")
    else:
        turtle.forward(pixels)

def backward(turtle, pixels=100):
    if not turtle.__class__ == Turtle:
        raise ValueError("forward(turtle, pixels): Input is not a turtle")
    if (None == pixels):
        turtle.backward()
    else:
        turtle.backward(pixels)

def moveTo(turtle, x, y):
    if not turtle.__class__ == Turtle:
		raise ValueError("forward(turtle, pixels): Input is not a turtle")
    turtle.moveTo(x,y)

def makeTurtle(world):
    if not (world.__class__ == World or world.__class__ == Picture):
        raise ValueError("makeTurtle(world): Input is not a world or picture")
    turtle = Turtle(world)
    return turtle

def penUp(turtle):
    if not turtle.__class__ == Turtle:
        raise ValueError("penUp(turtle): Input is not a turtle")
    turtle.penUp()

def penDown(turtle):
    if not turtle.__class__ == Turtle:
        raise ValueError("penDown(turtle): Input is not a turtle")
    turtle.penDown()

def getHeading(turtle):
    if not turtle.__class__ == Turtle:
        raise ValueError("getHeading(turtle): Input is not a turtle")
    return turtle.getHeading()

def getXPos(turtle):
	if not turtle.__class__ == Turtle:
		raise ValueError("getXPos(turtle): Input is not a turtle")
	return turtle.getXPos()

def getYPos(turtle):
	if not turtle.__class__ == Turtle:
		raise ValueError("getYPos(turtle): Input is not a turtle")
	return turtle.getYPos()

##
## Global world functions ------------------------------------------------------
##
def makeWorld(width=None, height=None):
    if(width and height):
        w = World(width, height)
    else:
        w = World()
    return w

def getTurtleList(world):
    if not world.__class__ == World:
        raise ValueError("getTurtleList(world): Input is not a world")
    return world.getModelsList()


##
## DEBUG -----------------------------------------------------------------------
##

# the following allows us to wrap an error message and display specific
# information depending on the context

def exceptionHook(type, value, traceback):
	try:
		global debugLevel
		curLevel = debugLevel
	except:
		curLevel = 0

	# handle each level
	if (curLevel == 0):
		# user mode
		print str(value)
		sys.exc_clear()
	elif (curLevel == 1):
		raise value
	else:
		# normal error mode
		tb = traceback
		framestack = []
		while tb:
			# get the current frame
			framestack.append(tb.tb_frame)
			# and traverse back to the top
			tb = tb.tb_next
		framestack.reverse()

		# print the message and each calling method
		print "Message: (%s)\n    %s" % (str(type), value)
		print "Stack Trace:"
		for tempFrame in framestack:
			print "    [%s:(%d)] - %s()" 	% 	(tempFrame.f_code.co_filename,
												tempFrame.f_lineno,
												tempFrame.f_code.co_name)
		sys.exc_clear()
# set the hook
sys.excepthook = exceptionHook


# graphical warnings and prompts
def showWarning(msg, title="Warning"):
	tkMessageBox.showwarning(title, msg)

def showError(msg, title="Error"):
	tkMessageBox.showerror(title, msg)

#
# all prompts return:
#	-1 for cancel (if there are > 2 choices)
#	0 for no/cancel (only if there are 2 choices)
# 	1 for yes/ok
#
def promptYesNo(promptMsg, title):
	result = tkMessageBox.askquestion(title, promptMsg, default=tkMessageBox.NO)
	if result == 'yes':
		return 1
	else:
		return 0

def promptOkCancel(promptMsg, title):
	return int(tkMessageBox.askokcancel(title, promptMsg, default=tkMessageBox.CANCEL))

#
# set the default debug level
# 0 - print user friendly error msgs only (default)
# 1 - throw normal errors
# 2 - show simple errors & stack trace
#
debugLevel = 0