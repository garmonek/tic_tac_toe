from game.field import Field
from game.serializable import Serializable

class Move(Serializable):
	field = None
	boardId = 0

	def __init__(self, x: int, y: int, boardId: int):
		self.field = Field(x, y)
		self.boardId = boardId

	@staticmethod
	def fromRequest(request: dict):
		move = request.get('move')
		return Move(**move) if move != None else None