from flask import Flask, render_template, request, redirect, url_for
from game import *
from game.tests.moves import *

MOVE_CMD = 'move'
RESTART_CMD = 'restart'

app = Flask(__name__)
game = Game()

@app.route("/")
def home():
	# v = game.validateMove(badMove1())
	# v = game.validateMove(goodMove())
	# for s in v:
	# 	print(s)
	# print(v.isEmpty())
	# print(v.toJSON())
	# game.move(badMove1())
	# print(game.toJSON())
	# print(game.turn)
	# game.move(goodMove())
	# print(game.turn)
	# moveDict = {'move':{'x':1, 'y':1,'boardId':1}}
	# move = Move.fromRequest(moveDict)
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

	if cmd == RESTART_CMD:
		game.__init__()

	return game.toJSON()
    
if __name__ == "__main__":
    app.run(debug=True)
