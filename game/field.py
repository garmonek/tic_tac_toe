from game.constants import BOARD_SIZE_RANGE
from game.sign import Sign

class Field():
	x = None
	y = None
	mark = None

	def __init__(self, x: int, y: int):		
		self.x = x
		self.y = y

	def __eq__(self, field):
		if self.x == field.x and self.y == field.y:
			return True
		return False

	def isInBoard(self)-> bool:
		if  not self.inBoardSize(self.x) or not self.inBoardSize(self.y):
			return False
		return True

	def inBoardSize(self, x: int)-> bool:
		if x not in BOARD_SIZE_RANGE:
			return False
		return True