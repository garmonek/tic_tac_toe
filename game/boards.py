from game.board import Board
from game.constants import BOARDS, BOARDS_RANGE
from game.sign import Sign
from game.move import Move

class Boards():
	boards = []

	def __init__(self):
		self.boards = [Board(x) for x in BOARDS_RANGE]
	
	def __iter__(self):
	    return iter(self.boards)
	 
	def getById(self, id: int)-> Board:
		if id not in BOARDS_RANGE:
			return None

		for board in self.boards:
			if board.id == id:
				return board
		return None

	def markField(self, move: Move, sign: Sign):
		board = self.getById(move.boardId)
		field = board.getField(move.field)
		field.mark = sign.value

	def updateWinner(self, turn: Sign):
		for board in self.boards:
			board.updateWinner(turn)