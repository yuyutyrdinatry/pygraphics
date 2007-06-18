import math
import media
import pygame

# TODO: one based indices???????

##
## MODEL DISPLAY --------------------------------------------------------------
##
class ModelDisplay:

	def notify(self):
		# To be implemented by derived function
		pass

	def getWidth(self):
		pass

	def getHeight(self):
		pass

##
## MODEL ----------------------------------------------------------------------
##
class Model:

	def paint(self, picture):
		# To be implemented by derived function
		pass

##
## PATH SEGMENT ---------------------------------------------------------------
##
class PathSegment(Model):

	def __init__(self, color, width, x1, y1, x2, y2):
		# set the segment properties
		self.color = color
		self.width = width
		self.startPoint = (x1, y1)
		self.endPoint = (x2, y2)

	def paint(self, picture):
		# we draw this segment in the color and width it was created with
		picture.addLine(self.color, self.startPoint[0], self.startPoint[1],
						self.endPoint[0], self.endPoint[1], self.width)

##
## PEN -------------------------------------------------------------------------
## The pen traces a number of path segments,
##
class Pen(Model):

	def __init__(self, color=media.green, width=1, down=True):
		# create the pen with the specified properties
		self.color = color
		self.width = width
		self.down = down
		self.pathSegmentList = []

	def isPenDown(self):
		# returns whether the pen is drawing or not
		return self.down

	def setPenDown(self, boolean):
		# sets the drawing state of the pen
		self.down = boolean

	def getColor(self):
		return color

	def setColor(self, color):
		self.color = color

	def getWidth(self):
		return width

	def setWidth(self, width):
		self.width = width

	def addMove(self, x1, y1, x2, y2):
		# we add a line (movement of the pen) if it is down, it uses the currently
		# set pen color and width
		if (self.down):
			ps = PathSegment(self.color, self.width, x1, y1, x2, y2)
			self.pathSegmentList.append(ps)

	def clearPath(self):
		# clear the paths that the pen has traced
		del self.pathSegmentList[:]

	def paint(self, picture):
		# draw the complete path which this pen has traced
		for path in self.pathSegmentList:
			path.paint(picture)

##
## WORLD ----------------------------------------------------------------------
## The world is able to hold a number of Model objects, one of which is the
## Turtle object.
##
class World(ModelDisplay, Model):

	backgroundColor = media.white
	backgroundImage = None

	def __init__(self, width=640, height=480, visible=True):
		# create and set the frame
		self.pictureFrame = media.Picture(True)
		self.pictureFrame.createImage(width, height)
		self.pictureFrame.clear(self.backgroundColor)
		self.pictureFrame.setTitle('World')
		self.models = []
		# if the world is visible, show the picture frame
		if (visible):
			self.pictureFrame.show()

	def addModel(self, model):
		# add a new model if it does not already exist
		if not self.containsModel(model):
			self.models.append(model)
			self.notify()

	def removeModel(self, model):
		# remove an existing model
		self.models.remove(model)
		self.notify()

	# NOTE: we are not using java, but can think of the Picture as a Graphics
	# Context where we can draw directly onto it, later we may want to extend
	# or wrap the Picture in an actual GraphicsContext which contains its own
	# affine space transformations
	def getPicture(self):
		return self.pictureFrame

	def clearBackground(self):
		self.pictureFrame.clear()

	def getBackgroundColor(self):
		return self.backgroundColor

	def setBackgroundColor(self, color):
		# set bg color and redraw
		self.backgroundColor =  color
		self.notify()

	def getBackgroundPicture(self):
		return self.backgroundImage

	def setBackgroundPicture(self, picture):
		# set bg image and redraw
		self.backgroundImage = picture
		self.notify()

	# implemented from Model
	def paint(self, picture):
		# for acceptable performance, we need to stop auto-repaint before continuing
		picture.setAutoRepaint(False)
		picture.clear(self.backgroundColor)
		# draw the bg image if there is one
		if self.backgroundImage != None:
			picture.overlayImage(self.backgroundImage)
		# update all objects in list
		for model in self.models:
			model.paint(picture)
		# remember to re-init auto repaint
		picture.setAutoRepaint(True)

	# implemented from ModelDisplay
	def notify(self):
		self.paint(self.pictureFrame)

	def getLastModel(self):
		# get the last model added
		if len(self.models) > 0:
			return self.models[len(self.models)-1]
		return None
	
	def getModelsList(self):
		return self.models

	def containsModel(self, model):
		return model in self.models

	def getWidth(self):
		return self.pictureFrame.getWidth()

	def getHeight(self):
		return self.pictureFrame.getHeight()

	def hideFrame(self):
		self.pictureFrame.hide()

	def showFrame(self):
		self.pictureFrame.repaint()

	def __str__(self):
		return "A %d by %d world with %d models in it." % (self.width, self.height, len(self.models))

##
## TURTLE ----------------------------------------------------------------------
##
class Turtle(Model):

	def __init__(self, modelDisplay, x=-1, y=-1, width=15, height=18):
		self.modelDisplay = modelDisplay
		# center the turtle horizontally if the x is not set
		if x < 0:
			self.x = modelDisplay.getWidth()/2
		else:
			self.x = x
		# center the turtle vertically if the y is not set
		if y < 0:
			self.y = modelDisplay.getHeight()/2
		else:
			self.y = y
		self.width = width
		self.height = height
		self.heading = 0
		self.pen = Pen()
		self.bodyColor = media.green
		self.shellColor = media.blue
		self.infoColor = media.black
		self.visible = True
		self.showInfo = False
		self.name = 'Turtle'
		# LASTLY, add to modeldisplay (world)
		self.modelDisplay.addModel(self)

	def getDistance(self, x, y):
		# return the euclidean distance of this turtle from a point
		dx = x-self.x
		dy = y-self.y
		return math.sqrt(pow(dx,2)+pow(dy,2))

	def turnToFace(self, turtle):
		# turn this turtle to face another turtle
		dx = turtle.getXPos()-self.x
		dy = turtle.getYPos()-self.y
		# offset heading by 90 degrees because we call north 0, also note that
		# in this coordinate frame, y is flipped (ie. 0,0 is topleft)
		self.heading = 90 - math.degrees(math.atan2(-dy, dx))
		# repaint
		self.updateDisplay()

	def setShowInfo(self, boolean):
		# set the name of the turtle
		self.showInfo = boolean

	def getShowInfo(self):
		# get the name of the turtle
		return self.showInfo

	def setShowInfo(self, boolean):
		# set whether to show the name or not
		self.showInfo = boolean
		# repaint
		self.updateDisplay()

	def getShellColor(self):
		return self.shellColor

	def setShellColor(self, color):
		self.shellColor = color
		# repaint
		self.updateDisplay()

	def getBodyColor(self):
		return self.bodyColor

	def setBodyColor(self, color):
		self.bodyColor = color
		# repaint
		self.updateDisplay()

	def setColor(self, color):
		self.setBodyColor(color)

	def getInfoColor(self):
		return self.infoColor

	def setInfoColor(self, color):
		self.infoColor = color
		# repaint
		self.updateDisplay()

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def setWidth(self, width):
		self.width = width
		# repaint
		self.updateDisplay()

	def setHeight(self, height):
		self.height = height
		# repaint
		self.updateDisplay()

	def getXPos(self):
		return self.x

	def setXPos(self, x):
		self.x = x
		# repaint
		self.updateDisplay()

	def getYPos(self):
		return self.y

	def setYPos(self, y):
		self.y = y
		# repaint
		self.updateDisplay()

	def setPos(self, x, y):
		self.x = x
		self.y = y
		# repaint
		self.updateDisplay()

	def getPen(self):
		return self.pen

	def setPen(self, pen):
		# NOTE: replaces the path of the old pen?
		self.pen = pen

	def isPenDown(self):
		return self.pen.isPenDown()

	def setPenDown(self, boolean):
		self.pen.setPenDown(boolean)

	def penUp(self):
		self.pen.setPenDown(False)

	def penDown(self):
		self.pen.setPenDown(True)

	def getPenColor(self):
		return self.pen.getColor()

	def setPenColor(self, color):
		self.pen.setColor(color)

	def setPenWidth(self, width):
		self.pen.setWidth(width)

	def getPenWidth(self):
		return self.pen.getWidth()

	def clearPath(self):
		self.pen.clearPath()
		# repaint
		self.updateDisplay()

	def getHeading(self):
		return self.heading

	def setHeading(self, heading):
		self.heading = heading
		# repaint
		self.updateDisplay()

	def getName(self):
		return self.name

	def setName(self, name):
		self.name = name

	def isVisible(self):
		return self.visible

	def setVisible(self, boolean):
		if (not self.visible and boolean):
			# update if now visible
			self.updateDisplay()
		self.visible = boolean

	def hide(self):
		self.setVisible(False)

	def show(self):
		self.setVisible(True)

	def updateDisplay(self):
		# ensure x/y >= 0
		self.x = max(0, self.x)
		self.y = max(0, self.y)

		# TODO: picture?
		if (self.modelDisplay != None):
			self.x = min(self.x, self.modelDisplay.getWidth()-1)
			self.y = min(self.y, self.modelDisplay.getHeight()-1)
			self.modelDisplay.notify()

	def forward(self, distance=100):
		# default is 100 pixels
		oldX = self.x
		oldY = self.y
		# calculate new x,y in heading, distance away
		self.x = oldX + (int)(distance * math.sin(math.radians(self.heading)))
		self.y = oldY + (int)(distance * -math.cos(math.radians(self.heading)))
		# add path
		self.pen.addMove(oldX, oldY, self.x, self.y)
		# refresh display
		self.updateDisplay()

	def backward(self, distance=100):
		self.forward(-distance)

	def moveTo(self, x, y):
		self.pen.addMove(self.x, self.y, x, y)
		self.x = x
		self.y = y
		self.updateDisplay()

	def turn(self, degrees):
		self.heading = (self.heading + degrees) % 360
		self.updateDisplay()

	def turnLeft(self):
		self.turn(-90)

	def turnRight(self):
		self.turn(90)

	def __rotateInPlace(self, surface, tlX, tlY, angle):
		# returns (surface, x,y) to draw the rotated surface
		surface = pygame.transform.rotate(surface, angle)
		surfaceCenter = surface.get_rect().center
		temp = (surface, tlX-surfaceCenter[0], tlY-surfaceCenter[1])
		return temp

	def paint(self, picture):
		if self.visible:
			# paint the path thus far
			self.pen.paint(picture)
			#
			x = self.x; y = self.y
			w = self.width; h = self.height
			#
			halfWidth = w/2
			quarterWidth = w/4
			sixWidth = w/6
			eightWidth = w/8
			#
			halfHeight = h/2
			thirdHeight = h/3
			twoThirdsHeight = (2*h)/3
			bodyHeightOffset = thirdHeight/2+twoThirdsHeight
			sixthHeight = h/6
			#
			bodyColor = self.bodyColor.getRGB()

			sprite = pygame.Surface((w,h), pygame.SRCALPHA, 32)
			# head
			pygame.draw.ellipse(sprite, bodyColor, pygame.Rect(halfWidth-quarterWidth/2,0,quarterWidth,thirdHeight))
			# feet
			feetWidth = quarterWidth
			feetOffset = math.sqrt(pow(feetWidth,2)/2)/2+twoThirdsHeight/2+thirdHeight
			pygame.draw.line(sprite, bodyColor, (feetOffset, thirdHeight/2+feetOffset), (w-feetOffset, h-feetOffset), feetWidth)
			pygame.draw.line(sprite, bodyColor, (feetOffset, h-feetOffset), (w-feetOffset, thirdHeight/2+feetOffset), feetWidth)
			# shell
			pygame.draw.ellipse(sprite, self.shellColor.getRGB(), pygame.Rect(sixWidth,thirdHeight/2, w-2*sixWidth,bodyHeightOffset))

			# rotate to heading
			postRot = self.__rotateInPlace(sprite, x, y, -self.heading)
			sprite = postRot[0]
			# copy to picture surface
			picture.surf.unlock()
			picture.surf.blit(sprite, (postRot[1], postRot[2]))
			picture.surf.lock()
			# draw info string
			self.drawInfoString(picture)

	def drawInfoString(self, picture):
		# draw the name
		picture.addText(self.infoColor, self.x + self.width, self.y, self.name)

	def __str__(self):
		return "%s turtle at %d, %d heading %f." % (self.name, self.x, self.y, self.heading)

