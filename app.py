from flask import Flask, render_template, request, redirect, url_for
from game import *
from game.tests.moves import *

MOVE_CMD = 'move'
RESTART_CMD = 'restart'

app = Flask(__name__)
game = Game()

@app.route("/")
def home():
	return render_template('index.html', game=game)

@app.route("/reset")
def reset():
	game.__init__()
	return redirect(url_for('home'))

@app.route("/hotSeat")
def hotSeat():
	game.__init__()
	game.deactivateBoot()
	return redirect(url_for('home'))

@app.route("/vsBot")
def vsBot():
	game.__init__()
	game.activateBot()
	return redirect(url_for('home'))

@app.route("/ajax", methods = ['POST'])
def ajax():
	req = request.get_json()
	cmd = req.get('cmd')
	if cmd == MOVE_CMD:
		move = Move.fromRequest(req)
		if move == None:
			return game.toJSON()
		
		game.move(move)		
		if not game.violations.isEmpty() or game.winner != None:
			return game.toJSON()

		if game.bootIsActive == True:
			botMove = Bot(game).createMove()
			game.move(botMove)

	return game.toJSON()
    
if __name__ == "__main__":
	app.run( port=5002, debug=True)
