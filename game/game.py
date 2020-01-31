from game.sign import Sign
from game.boards import Boards
from game.move import Move
from game.violations import Violations
from game.serializable import Serializable
from game.constants import BOARDS, BOARD_SIZE, FIELD_OUT_OF_BOARD, FIELD_ALREADY_MARKED, NO_SUCH_BOARD, CAN_MARK_INACTIVE_BOARD
from game.board import Board

class Game(Serializable):
	turn = None
	boards = None
	current_board = None
	winned_boards_x = []
	winned_boards_o = []
	winner = None
	violations = None
	activeBoardId = None

	def __init__(self, sign: Sign=Sign.X):
		self.turn = sign
		self.boards = Boards()
		self.violations = Violations()
		self.winned_boards_o = []
		self.winned_boards_x = []
		self.winner = None
		self.activeBoardId = None
	
	def move(self, move: Move):
		if self.winner:
			return

		self.violations = self.__validateMove(move)
		if not self.violations.isEmpty():
			return

		self.boards.markField(move, self.turn)
		self.__updateWinner(self.turn)
		self.__updateActiveBoard(move)
		self.__changeTurn()

	def __validateMove(self, move: Move)-> Violations:
		violations = Violations()
		if not move.field.isInBoard():
			violations.add(FIELD_OUT_OF_BOARD)
		#todo to remove
		# if move.boardId in self.winned_boards_x or move.boardId in self.winned_boards_o:
		# 	violations.add(BOARD_ALREADY_WINNED)

		if self.activeBoardId != None and move.boardId != self.activeBoardId:
			violations.add(CAN_MARK_INACTIVE_BOARD)

		board = self.boards.getById(move.boardId)
		if board == None:
			violations.add(NO_SUCH_BOARD)

		if board.getField(move.field).mark != None:
			violations.add(FIELD_ALREADY_MARKED)

		return violations


	def __updateActiveBoard(self, move: Move):
		self.activeBoardId = self.__getActiveBoardIdByXY(move.field.x, move.field.y)

	def __updateWinner(self, turn: Sign):
		self.boards.updateWinner(self.turn)
		self.__updateWinnedBoards()
		winnedBoard = self.__getWinnedBoardsBySign(turn)
		if len(winnedBoard) > (BOARDS // 2):
			self.winner = turn

	def __updateWinnedBoards(self):
		for board in self.boards:
			winner = board.getWinner()
			if winner != None:
				self.__addToWinnedBoards(board)

	def __addToWinnedBoards(self, board: Board):
		winnedBoard = self.__getWinnedBoardsBySign(board.winner)
		if board.id not in winnedBoard:
			winnedBoard.append(board.id)

	def __getWinnedBoardsBySign(self, sign: Sign):
		return self.winned_boards_x if sign == Sign.X else self.winned_boards_o

	def __changeTurn(self):
		self.turn = Sign.opposite(self.turn)
	
	def __getActiveBoardIdByXY(self, x:int, y:int)-> int:
		return (y-1)*BOARD_SIZE + x;