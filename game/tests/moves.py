from game.move import Move

def outOfBoardMove()-> Move:
	return Move(-1, 2, 1)

def badMove1()-> Move:
	return Move(3, 4, 1)

def goodMove()-> Move:
	return Move(1, 2, 1)