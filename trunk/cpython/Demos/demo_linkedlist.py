from media import *

# from demo_linkedlist import *; llv = LinkedListViewer(640, 480);

def getTextDimensions(string):
	global defaultFont
	return defaultFont.size(string)

def getBezierPoint(ax, bx, cx, ay, by, cy, cp, i, num):
	t = i*1.0/num
	tSquared = t * t
	tCubed = tSquared * t
	
	x = (ax * tCubed) + (bx * tSquared) + (cx * t) + cp[0][0]
	y = (ay * tCubed) + (by * tSquared) + (cy * t) + cp[0][1]
	return (x,y)

def drawBezierCurve(picture, cp, width=1):	
	cx = 3.0 * (cp[1][0] - cp[0][0])
	bx = 3.0 * (cp[2][0] - cp[1][0]) - cx
	ax = cp[3][0] - cp[0][0] - cx - bx	    
	cy = 3.0 * (cp[1][1] - cp[0][1])
	by = 3.0 * (cp[2][1] - cp[1][1]) - cy
	ay = cp[3][1] - cp[0][1] - cy - by
	
	num = 7
	for i in range(0, num):
		(x,y) = getBezierPoint(ax,bx,cx,ay,by,cy,cp, i, num)
		(xP,yP) = getBezierPoint(ax,bx,cx,ay,by,cy,cp, i+1, num)		
		picture.addLine(red, x, y, xP, yP, width)
    
class Button:
	padding = 10

	def __init__(self, x, y, text, actionCallback):
		self.x = x
		self.y = y
		self.text = text
		self.callback = actionCallback
		(self.width, self.height) = getTextDimensions(text)

	def intersects(self, x, y):
		return (self.x < x and x < self.x+self.width+self.padding
				and self.y < y and y < self.y+self.height+self.padding)

	def execute(self):
		self.callback()

	def paint(self, picture):
		pad = self.padding
		picture.addRect(blue, self.x, self.y, self.width+pad, self.height+pad)
		picture.addText(red, self.x+pad/2, self.y+pad/2, self.text)

class Node:
	width = 60
	height = 30
	dotRadius = 5
	prev = None
	next = None
	bgColor = white

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def intersects(self, x, y):
		return self.intersectsOutgoingLink(x, y) or self.intersectsIncomingLink(x, y)

	def intersectsIncomingLink(self, x, y):
		return (self.x < x and x < self.x+self.width/2
				and self.y < y and y < self.y+self.height)

	def intersectsOutgoingLink(self, x, y):
		return (self.x+self.width/2 < x and x < self.x+self.width
				and self.y < y and y < self.y+self.height)

	def paint(self, picture, isCurrent=False):
		# picture.addRectFilled(self.bgColor, self.x, self.y, self.width, self.height)
		picture.addLine(blue, self.x+self.width/2, self.y, self.x+self.width/2, self.y+self.height, 3)
		if isCurrent:
			picture.addRect(yellow, self.x, self.y, self.width, self.height, 3)
		else:
			picture.addRect(blue, self.x, self.y, self.width, self.height, 3)
		picture.addOvalFilled(green, self.x+(self.width*3)/4-self.dotRadius, self.y+self.height/2-self.dotRadius, 2*self.dotRadius, 2*self.dotRadius)
		if self.next != None:
			x = self.x+(self.width*3)/4
			y = self.y+self.height/2
			if self.next.x >= self.x:	# arrow from left
				drawBezierCurve(picture, ( (x,y), ((x+self.next.x)/2,y), ((x+self.next.x)/2, self.next.y+(self.next.height/2)), (self.next.x, self.next.y+(self.next.height/2)) ), 3)
				picture.addLine(red, self.next.x, self.next.y+(self.height/2), self.next.x-5, self.next.y+(self.next.height/2)-5, 3)
				picture.addLine(red, self.next.x, self.next.y+(self.height/2), self.next.x-5, self.next.y+(self.next.height/2)+5, 3)
			else:						# arrow from right
				drawBezierCurve(picture, ( (x,y), ((x+self.next.x)/2,y), ((x+self.next.x+self.next.width)/2, self.next.y+(self.next.height)), (self.next.x+self.next.width, self.next.y+(self.next.height)) ), 3)
				picture.addLine(red, self.next.x+self.next.width, self.next.y+(self.height), self.next.x+self.next.width+5, self.next.y+(self.next.height)-5, 3)
				picture.addLine(red, self.next.x+self.next.width, self.next.y+(self.height), self.next.x+self.next.width+5, self.next.y+(self.next.height)+5, 3)

class LinkedListViewer:
	nodes = []
	buttons = []
	curNode = None
	offset = 80
	draggingOne = False
	draggingTwo = False	

	def __init__(self, w, h):
		self.picture = Picture()
		self.picture.createImage(w, h)
		self.picture.addEventHandler("<Button-1>", self.onClick)
		self.picture.addEventHandler("<B1-Motion>", self.onDrag)
		self.picture.addEventHandler("<B2-Motion>", self.onMove)
		self.picture.addEventHandler("<ButtonRelease>", self.onDrop)
		# default buttons
		self.buttons.append(Button(10, 10, 'Add Node', self.addNode))
		self.buttons.append(Button(10, 40, 'Next', self.visitNextNode))
		self.picture.show()
		self.repaint()

	def onClick(self, event):
		for button in self.buttons:	# check buttons
			if button.intersects(event.x, event.y):
				button.execute()
				break
		for node in self.nodes:		# check nodes
			if node.intersects(event.x, event.y):
				self.curNode = node
				self.repaint()

	def onDrag(self, event):
		if not self.draggingOne:
			for node in self.nodes:		# check nodes
				if node.intersectsOutgoingLink(event.x, event.y):
					self.curNode = node
					self.draggingOne = True
					break
				elif node.intersectsIncomingLink(event.x, event.y) and node.prev != None:
					self.curNode = node.prev
					print self.curNode
					self.draggingOne = True
					break
		else:											# we are in the middle of dragging, so draw line
			self.prevX = event.x
			self.prevY = event.y
			self.repaint()
		
	def onMove(self, event):
		if not self.draggingTwo:			# first right button down
			for node in self.nodes:		# check nodes
				if node.intersects(event.x, event.y):	
					self.moveNode = node
					self.draggingTwo = True
					self.prevX = event.x
					self.prevY = event.y	
					break
		else:
			self.moveNode.x = self.moveNode.x + event.x - self.prevX
			self.moveNode.y = self.moveNode.y + event.y - self.prevY
			self.prevX = event.x
			self.prevY = event.y	
			self.repaint()
			

	def onDrop(self, event):
		if event.num == 1:
			# find node to drop to
			self.draggingOne = False			
			for node in self.nodes:
				if node.intersectsIncomingLink(event.x, event.y) and node != self.curNode and self.curNode != None:				
					self.curNode.next = node
					node.prev = self.curNode
			self.repaint()								
		self.draggingTwo = False

	def addNode(self):
		node = Node(self.offset, self.offset)
		self.offset = (self.offset + 80) % (self.picture.getHeight()-50)
		self.nodes.append(node)
		self.curNode = node
		self.repaint()

	def visitNextNode(self):
		if self.curNode != None and self.curNode.next != None:
			self.curNode = self.curNode.next
			self.repaint()

	def repaint(self):
		self.picture.setAutoRepaint(False)
		self.picture.clear()
		for node in self.nodes:		# draw nodes
			node.paint(self.picture, (self.curNode == node))
		for button in self.buttons:	# draw buttons
			button.paint(self.picture)
		if self.draggingOne and self.curNode != None:
			x = self.curNode.x+(self.curNode.width*3)/4
			y = self.curNode.y+self.curNode.height/2
			drawBezierCurve(self.picture, ( (x,y), ((x+self.prevX)/2,y), ((x+self.prevX)/2, self.prevY), (self.prevX, self.prevY) ), 3)
		self.picture.setAutoRepaint(True)
