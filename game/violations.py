from game.serializable import Serializable

class Violations(Serializable):
	messages = []

	def __init__(self):
		self.messages = []

	def __iter__(self):
	    return iter(self.messages)

	def add(self, message: str):
		self.messages.append(message)

	def isEmpty(self)-> bool:
		return len(self.messages) == 0