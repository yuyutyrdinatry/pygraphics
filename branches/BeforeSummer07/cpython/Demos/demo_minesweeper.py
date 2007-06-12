from media import *
from Numeric import zeros
import random

# from demo_minesweeper import *; a = Minesweeper()

class Tile:
	visible = False
	surroundingCount = 0;

class Minesweeper:	
		
	boardWidth = 20
	boardHeight = 10
	tileSize = 30
	numberOfBombs = 15
	backFaceColor = Color(150,150,150)
	emptyFaceColor = Color(210,210,210)
	gameOver = False	
		
	def __init__(self):
		self.font = makeStyle("Times", fontsize=32)
		self.picture = Picture()
		self.width = (self.boardWidth-1) + (self.boardWidth*self.tileSize)			# add one pixel per line between columns
		self.height = (self.boardHeight-1) + (self.boardHeight*self.tileSize)	# add one pixel per line between rows
		self.picture.createImage(self.width, self.height)										# create empty picture
		self.picture.setTitle('Minesweeper');
		self.picture.addEventHandler("<Button-1>", self.onClick)
		self.picture.addEventHandler("<Button-2>", self.onReset)
		self.createBoard()		

	def createBoard(self):
		self.picture.clear(black)
		self.board =  Numeric.zeros([self.boardWidth,self.boardHeight])
		self.visible =  Numeric.zeros([self.boardWidth,self.boardHeight])
		# create bombs
		for i in range(self.numberOfBombs):
			self.board[random.randint(0,self.boardWidth-1)][random.randint(0,self.boardHeight-1)] = -1;
		# count bombs surrounding each tile
		for i in range(self.boardWidth):
			for j in range(self.boardHeight):
				if (self.board[i][j] > -1):		# if not a bomb
					self.board[i][j] = self.countSurroundingTiles(i, j)
		self.redraw()
				
	def countSurroundingTiles(self, x, y):
		count = 0
		for i in range(max(0, x-1), min(x+1,self.boardWidth-1)+1):
			for j in range(max(0, y-1), min(y+1,self.boardHeight-1)+1):
				if self.board[i][j] < 0:
					count = count+1
		return count

	def drawTile(self, x, y):
		xP = (x*(self.tileSize+1))
		yP = (y*(self.tileSize+1))
		if self.visible[x][y] == 0:				# unopened tiles
			self.picture.addRectFilled(self.backFaceColor, xP+1, yP+1, self.tileSize, self.tileSize);
		else:
			self.picture.addRectFilled(self.emptyFaceColor, xP+1, yP+1, self.tileSize, self.tileSize);
			if (self.board[x][y] < 0):			# mines
				self.picture.addTextWithStyle(red, xP+10, yP+6, 'x', self.font)
			elif (self.board[x][y] > 0):		# numbered tile
				self.picture.addTextWithStyle(blue, xP+10, yP+6, str(self.board[x][y]), self.font)
				
	def redraw(self):
		self.picture.setAutoRepaint(False)
		# draw grid
		i = self.tileSize+1		
		while i < self.width:
			self.picture.addLine(green, i, 1, i, self.height)
			i = i+self.tileSize+1
		j = self.tileSize+1
		while j < self.height:
			self.picture.addLine(green, 1, j, self.width, j)
			j = j+self.tileSize+1
		# draw tiles
		for i in range(self.boardWidth):
			for j in range(self.boardHeight):
				self.drawTile(i, j)
		self.picture.setAutoRepaint(True)		# automatically redraws
		self.picture.repaint()
		
	def clearSurroundingTiles(self, x, y):	
		if (self.board[x][y] == 0):		# then clear all surround which are not bombs
			self.visible[x][y] = 1	
			self.drawTile(x,y)
			for i in range(max(0, x-1), min(x+1,self.boardWidth-1)+1):
				for j in range(max(0, y-1), min(y+1,self.boardHeight-1)+1):
					if not (i == x and j == y) and self.visible[i][j] == 0:
						self.clearSurroundingTiles(i, j)
		elif (self.board[x][y] > 0):
			self.visible[x][y] = 1	
			self.drawTile(x,y)

	def onClick(self, event):
		self.picture.setAutoRepaint(False)
		x = event.x/(self.tileSize+1)
		y = event.y/(self.tileSize+1)
		# update self
		self.visible[x][y] = 1
		self.drawTile(x,y)
		# update board
		if (self.board[x][y] < 0):			# a mine - game over, show all mines
			for i in range(self.boardWidth):
				for j in range(self.boardHeight):
					if (self.board[i][j] < 0):		
						self.visible[i][j] = 1
						self.drawTile(i,j)
			self.gameOver = True
		elif (self.board[x][y] == 0):	# is empty
			self.clearSurroundingTiles(x,y)
		else:											# is a numbered tile
			pass
		# check if the game is over
		visibleCount = 0
		for i in range(self.boardWidth):
			for j in range(self.boardHeight):
				if (self.visible[i][j] == 0):		
					visibleCount = visibleCount+1
		if (visibleCount == self.numberOfBombs):
			self.picture.addTextWithStyle(red, 100, 100, 'YOU WIN!', self.font)
			self.gameOver = True
		self.picture.setAutoRepaint(True)		# automatically redraws

	def onReset(self, event):
		if (self.gameOver):
			self.createBoard()
			self.gameOver = False
				
	
	

