from game import Game
from game.move import Move
from game.moveStat import MoveStat
from copy import deepcopy
from game.constants import BOARD_SIZE, BOARDS, BOT_MAX_RECURSION

class Bot():
	game = None
	moveStats = []
	maxRecursion = BOT_MAX_RECURSION

	def __init__(self, game: Game):
		self.game = deepcopy(game)
		self.moveStats = []
		self.maxRecursion = BOT_MAX_RECURSION

	def createMove(self)-> Move:
		self.moveStats = self.createMoveStats(self.game)
		for moveStat in self.moveStats:
			self.maxRecursion = BOT_MAX_RECURSION
			self.recursiveSetMoveStats(self.game, moveStat)
		return self.getMoveWithBestStat()

	def getMoveWithBestStat(self):
		moveStats = deepcopy(self.moveStats)
		if 0 == len(moveStats):
			raise ValueError('Length of self.moveStats is 0!?')

		sortedMoveStats = sorted(moveStats, key=lambda moveStat: moveStat.stat)
		return sortedMoveStats.pop().move

	def recursiveSetMoveStats(self, game: Game, moveStat: MoveStat):
		game = deepcopy(game)
		game.move(moveStat.move)
		self.updateStats(game, moveStat)

		self.maxRecursion -= 1
		if self.maxRecursion <= 0:
			return

		for newMoveStat in self.createMoveStats(game, moveStat.id):
			return self.recursiveSetMoveStats(game, newMoveStat)

	def updateStats(self, game: Game, moveStat: MoveStat):
		if len(game.winnedBoardsX) != len(self.game.winnedBoardsX):
			self.addToMoveStatWithId(moveStat.id, -1)
		if len(game.winnedBoardsO) != len(self.game.winnedBoardsO):
			self.addToMoveStatWithId(moveStat.id, 1)


	def addToMoveStatWithId(self, id: int, value: int):
		moveStat = self.getMoveStatById(id)
		moveStat.stat+=value
		

	def getMoveStatById(self, id: int)-> MoveStat:
		for moveStat in self.moveStats:
			if moveStat.id == id:
				return moveStat
		raise ValueError('MoveStat with id:%d not found' %id)

	def createMoveStats(self, game: Game, parentMoveStatId = None):
		id = 1
		moveStats = []
		for move in self.createMoves(game):
			moveStat = MoveStat(parentMoveStatId, move) if isinstance(parentMoveStatId, int) else MoveStat(id, move)
			moveStats.append(moveStat)
			id+=1;
		return moveStats

	def createMoves(self, game: Game):
		moves = []
		for board in self.getBoardsForMove(game):
			for field in board.getUnmarkedFields():
				move = Move(field.x, field.y, board.id)
				violations = game.validateMove(move)
				if violations.isEmpty():
					moves.append(move)
		return moves

	def getBoardsForMove(self, game: Game)-> list:
		activeBoardId = game.activeBoardId
		if activeBoardId != None:
			return [game.boards.getById(activeBoardId)]

		return game.boards.getNotWinnedBoards()