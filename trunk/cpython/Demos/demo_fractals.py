from turtle import *;
import math

# from demo_fractals import *; k = KochSnowflake()

class KochSnowflake:
	radius = 270
	n = 4
	
	def __init__(self):
		self.world = World()
		self.turtle = Turtle(self.world, width=30, height=40)
		self.turtle.setName('Kochy')
		self.theta = (2.0*math.pi)/self.n
		#
		self.turtle.turn(270)
		self.turtle.forward(self.radius)
		self.turtle.turn(90+math.degrees(self.theta/2))
		#
		for i in range(self.n):
			# first line
			self.recDrawKochCurve(0, self.radius, i)
			self.turtle.turn(math.degrees(self.theta))
			#
			
	def recDrawKochCurve(self, curDepth, length, maxDepth):
		if curDepth == maxDepth:
			self.turtle.forward(length)
		else:
			# flat line			
			self.recDrawKochCurve(curDepth+1, length/3, maxDepth)
			# rise
			self.turtle.turn(-60)
			self.recDrawKochCurve(curDepth+1, length/3, maxDepth)
			# fall
			self.turtle.turn(120)
			self.recDrawKochCurve(curDepth+1, length/3, maxDepth)
			# flat line
			self.turtle.turn(-60)
			self.recDrawKochCurve(curDepth+1, length/3, maxDepth)
		
#from demo_fractals import *; s = SierpinskiTriangle()		
		
class SierpinskiTriangle:
	length = 256
	n = 4
	
	def __init__(self):
		self.world = World()
		self.turtle = Turtle(self.world, width=30, height=40)
		self.turtle.setName('Sierpy')
		#
		self.turtle.turn(30)
		self.turtle.setPos(100, 400)
		#
		self.recDrawSierpinski(0, self.turtle.getXPos(), self.turtle.getYPos(),self.length, self.n)
			
	def recDrawSierpinski(self, curDepth, x, y, length, maxDepth):
		if curDepth == maxDepth:
			self.turtle.forward(length)
			self.turtle.turn(120)
			self.turtle.forward(length)
			self.turtle.turn(120)
			self.turtle.forward(length)
			self.turtle.turn(120)
		else:
			# top triangle			
			self.turtle.setPos(x+length/4, y-length/2)
			self.recDrawSierpinski(curDepth+1, x+length/4, y-length/2, length/2, maxDepth)			
			# left triangle
			self.turtle.setPos(x,y)
			self.recDrawSierpinski(curDepth+1, x, y, length/2, maxDepth)
			#right triangle
			self.turtle.setPos(x+length/2, y)
			self.recDrawSierpinski(curDepth+1, x+length/2, y, length/2, maxDepth)
		