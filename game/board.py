from itertools import product
from game.field import Field
from game.constants import BOARD_SIZE, BOARD_SIZE_RANGE
from game.sign import Sign

class Board():
	id = None
	winner = None
	fields = []

	def __init__(self, id: int):
		self.id = id
		self.fields = [Field(x, y) for y,x in product(BOARD_SIZE_RANGE, repeat = 2)]		

	def getField(self, input_field: Field)-> Field:
		for field in self.fields:
			if field == input_field:
				return field

	def updateWinner(self, turn: Sign):
		markedFields = self.getMarkedFields(turn)
		if self.winByColumn(markedFields) or self.winByRow(markedFields) or self.winByDiagonal(markedFields):
			self.winner = turn

	def getWinner(self)-> Sign:
		return self.winner

	def getMarkedFields(self, sign: Sign)-> list:
		return [field for field in self.fields if field.mark == sign.value]

	def winByDiagonal(self, fields: list)-> bool:
		differences = [field.x - field.y for field in fields]
		if differences.count(0) == BOARD_SIZE:
			return True
		reversedXDifference = [(BOARD_SIZE - field.x + 1) - field.y for field in fields]
		if reversedXDifference.count(0) == BOARD_SIZE:
			return True
		return False

	def winByColumn(self, fields: list)-> bool:
		xValues = [field.x for field in fields]
		return self.winInRow(xValues)

	def winByRow(self, fields: list)-> bool:
		yValues = [field.y for field in fields]
		return self.winInRow(yValues)

	def winInRow(self, direction: list)-> bool:
		for x in BOARD_SIZE_RANGE:
			count = direction.count(x)
			if count == BOARD_SIZE:
				return True
		return False