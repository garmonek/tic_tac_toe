from game.sign import Sign
from game.boards import Boards
from game.move import Move
from game.violations import Violations
from game.serializable import Serializable
from game.constants import BOARDS, BOARD_SIZE, FIELD_OUT_OF_BOARD, FIELD_ALREADY_MARKED, NO_SUCH_BOARD, CAN_MARK_INACTIVE_BOARD, BOARD_ALREADY_WINNED
from game.board import Board

class Game(Serializable):
	turn = None
	boards = None
	current_board = None
	winnedBoardsX = []
	winnedBoardsO = []
	winner = None
	violations = None
	activeBoardId = None
	bootIsActive = False

	def __init__(self, sign: Sign=Sign.X):
		self.turn = sign
		self.boards = Boards()
		self.violations = Violations()
		self.winnedBoardsO = []
		self.winnedBoardsX = []
		self.winner = None
		self.activeBoardId = None
	
	def activateBot(self):
		self.bootIsActive = True

	def deactivateBoot(self):
		self.bootIsActive = False

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

		if self.__boardIsWinned(move.boardId):
			violations.add(BOARD_ALREADY_WINNED)

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
		if self.__boardIsWinned(self.activeBoardId):
			self.activeBoardId = None

	def __updateWinner(self, turn: Sign):
		self.boards.updateWinner(self.turn)
		self.__updateWinnedBoards()
		winnedBoard = self.__getWinnedBoardsBySign(turn)
		if len(winnedBoard) >= BOARD_SIZE:
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
		return self.winnedBoardsX if sign == Sign.X else self.winnedBoardsO

	def __changeTurn(self):
		self.turn = Sign.opposite(self.turn)
	
	def __getActiveBoardIdByXY(self, x:int, y:int)-> int:
		return (y-1)*BOARD_SIZE + x;

	def __boardIsWinned(self, boardId: int):
		return True if boardId in (self.winnedBoardsX + self.winnedBoardsO) else False