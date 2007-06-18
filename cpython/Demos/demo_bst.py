from media import *
import tkSimpleDialog

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
		picture.addRect(black, self.x, self.y, self.width+pad, self.height+pad)
		picture.addText(blue, self.x+pad/2, self.y+pad/2, self.text)

class Node:
	width = 60
	height = 30	
	left = None
	right = None
	visited = True
	value = 0
	
	def __init__(self, val):
		self.value = val

	def paint(self, picture, x, y, curNum):
		valueStr = ""
		if (self.visited):
			if (int(self.value) < int(curNum)):				# set value str
				valueStr = "> "
			elif (int(self.value) == int(curNum)): 
				valueStr = "= "
			else:
				valueStr = "< "
		valueStr += str(self.value)
		(w, h) = getTextDimensions(valueStr)			# draw the nodes
		if self.visited:
			picture.addRect(tomato, x-(self.width/2), y, self.width, self.height, 3)
		else:	
			picture.addRect(blue, x-(self.width/2), y, self.width, self.height, 3)
		picture.addText(blue, x-w/2, y+h/2, valueStr)

class BSTViewer:
	buttons = []
	root = None
	newNumber = 0

	def __init__(self, w, h):
		self.picture = Picture()
		self.picture.createImage(w, h)
		self.picture.addEventHandler("<Button-1>", self.onClick)
		# default buttons
		self.buttons.append(Button(10, 10, 'Add Node', self.addNode))
		self.picture.show()
		self.addNode(50)
		self.addNode(75)
		self.addNode(80)
		self.addNode(25)
		self.addNode(5)
		self.resetNode(self.root)
		self.repaint()
		self.picture.frame.wait_window()
		
	def onClick(self, event):
		for button in self.buttons:	# check buttons
			if button.intersects(event.x, event.y):
				button.execute()
				break

	def addNode(self, val=None):
		if val == None:
			self.newNumber = tkSimpleDialog.askinteger("", "Enter a number:")		
		else:
			self.newNumber = val
		self.resetNode(self.root)					# unvisit all nodes
		if (self.root == None):	
			self.root = Node(self.newNumber)
		self.insertValue(self.root, self.newNumber)
		self.repaint()
	
	def insertValue(self, node, value):		
		node.visited = True
		if (int(node.value) == int(value)):			
			pass
		elif (int(value) > int(node.value)):
			if (node.right == None):
				node.right = Node(value)
				return
			else:
				self.insertValue(node.right, value)
		else:		
			if (node.left == None):
				node.left = Node(value)
				return
			else:
				self.insertValue(node.left, value)
		
	def resetNode(self, node):
		if (node == None):
			return
		node.visited = False
		self.resetNode(node.left)
		self.resetNode(node.right)

	def paintNode(self, node, x, y):
		node.paint(self.picture, x, y, self.newNumber)		# paint this node
		if (node.left != None):
			self.paintNode(node.left, x-60, y+60)		# paint left child
			self.picture.addLine(black, x, y+node.height, x-60, y+60, 3)
		if (node.right != None):
			self.paintNode(node.right, x+60, y+60)		# paint right child
			self.picture.addLine(black, x, y+node.height, x+60, y+60, 3)

	def repaint(self):		
		self.picture.setAutoRepaint(False)
		self.picture.clear(white)
		self.paintNode(self.root, 240, 10)
		for button in self.buttons:	
			button.paint(self.picture)			# draw buttons
		self.picture.setAutoRepaint(True)


