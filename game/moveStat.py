from game.move import Move

class MoveStat():
	id = None
	move = None
	stat = 0

	def __init__(self, id: int, move: Move, stat: int = 0):
		self.move = move
		self.stat = 0
		self.id = id

